<template>
  <div>
    <v-card flat tile append :disabled="busy" class="graph" id="graph">
      <v-snackbar
        v-model="message.visible"
        :color="message.color"
        :timeout="5000"
        top
      >{{message.text}}</v-snackbar>
      <v-overlay :value="busy">
        <v-progress-circular :size="200" :width="8" indeterminate color="primary"></v-progress-circular>
      </v-overlay>
    </v-card>
    <v-fab-transition transition="scale-transition" v-for="(item,i) in menu" :key="'buttons-' + i">
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            :style="{top: menu[i].position.y, left: menu[i].position.x}"
            fab
            absolute
            @click="button(item.fn, item.target)"
            v-on="on"
          >
            <v-icon>{{item.icon}}</v-icon>
          </v-btn>
        </template>
        <span v-html="item.name"></span>
      </v-tooltip>
    </v-fab-transition>
    <properties ref="properties" :element_properties="element_properties"></properties>
    <search
      ref="search"
      @add_element="add_element"
      @remove_element="remove_element"
      @show="show"
      @find_actions="find_actions"
      :hide="hide"
      :alt="events.alt"
    ></search>
    <v-dialog max-width="550" modal v-model="limit.display">
      <v-card>
        <v-card-title class="headline py-5">Eish...</v-card-title>

        <v-card-text class="text-md-left">
          Query returned
          <b>{{limit["size"]}}</b> results. The UI will probably break while trying to render such a large graph.
          Consider refining your search by using Neo4j (http://localhost:7474) directly.
          <br />
          <br />The query that was issued was:
          <br />
          <br />
          <b>{{limit["query"]}}</b>
        </v-card-text>

        <v-card-actions>
          <v-btn outlined color="green darken-1" @click="limit.display = false" text>Cancel</v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="add_element_continue(limit.elements)"
          >Roll the dice!</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import properties from "@/components/properties";
import search from "@/components/search";
import config from "@/config.js";

import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";

let cy = null;

export default {
  name: "Graph",
  components: { properties, search },

  data: function() {
    return {
      limit: {
        threshold: 500,
        display: false,
        elements: [],
        query: "",
        size: 0
      },
      message: {
        visible: false,
        text: "",
        color: "success"
      },
      loading: {
        query: false,
        graph: false,
        enabled: true
      },
      events: {
        menu: {},
        select: {},
        alt: false,
        ctrl: false
      },
      elements: [],
      hide: false,
      element_properties: null,
      buttons: [
        {
          name: "Outbound <b>Paths</b>",
          icon: "mdi-map-marker-up",
          fn: this.find_paths_from
        },
        {
          name: "Outbound <b>Actions</b>",
          icon: "mdi-file-search",
          fn: this.find_actions_from
        },
        {
          name: "Inbound <b>Paths</b>",
          icon: "mdi-map-marker-outline",
          fn: this.find_paths_to
        },
        {
          name: "Inbound <b>Actions</b>",
          icon: "mdi-file-search-outline",
          fn: this.find_actions_to
        }
      ]
    };
  },

  methods: {
    show() {
      this.hide = !this.hide;
    },

    find_paths_to(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);

      return this.query(
        "MATCH (source)-[:TRANSITIVE|ATTACK]->(), (target) " +
          `WHERE ID(target) = ${id} AND (source:External OR source:Resource)  ` +
          "WITH source, target " +
          "MATCH paths=shortestPath((source)-[:TRANSITIVE|ATTACK*0..]->(target)) " +
          "RETURN paths"
      );
    },

    find_paths_from(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);
      return this.query(
        `MATCH (source) WHERE ID(source) = ${id} ` +
          "OPTIONAL MATCH path=shortestPath((source)-[:TRANSITIVE|ATTACK*0..]->(target)) " +
          "WHERE (target:Resource OR target:Admin) " +
          "AND source <> target " +
          "RETURN source, path"
      );
    },

    find_actions(actions) {
      this.query(
        `WITH "${actions}" AS action ` +
          "MATCH path=()-[:ACTION{Name:action}]->() RETURN path"
      ).then(elements => {
        this.add_element(elements);
      });
    },

    find_actions_to(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);

      return this.query(
        `MATCH (target) WHERE ID(target) = ${id} ` +
          "OPTIONAL MATCH actions=(_)-[:ACTION]->(target) " +
          "WHERE (_:Resource OR _:External) " +
          "RETURN target, actions"
      );
    },

    find_actions_from(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);

      return this.query(
        `MATCH (source) WHERE ID(source) = ${id} ` +
          "OPTIONAL MATCH actions=(source)-[:ACTION]->(:Resource) " +
          "RETURN source, actions"
      );
    },

    collapse_actions_all() {
      let elements = [];
      let actions = {};
      cy.edges((e, i) => e.hasClass("ACTION")).map(a => {
        if (!(a.data("source") in actions)) actions[a.data("source")] = [];
        if (!(a.data("target") in actions[a.data("source")])) {
          actions[a.data("source")].push(a.data("target"));
          elements.push(a);
        }
      });
      this.collapse_actions(elements);
    },

    collapse_actions(elements) {
      let add = [];
      let remove = [];

      elements.map(element => {
        let source = element.data("source");
        let target = element.data("target");
        let edges = cy.edges((e, i) => {
          return (
            e.hasClass("ACTION") &&
            e.data("source") == source &&
            e.data("target") == target
          );
        });
        let collection = {};
        edges.jsons().forEach(e => {
          if (!(e.data.properties.Access in collection))
            collection[e.data.properties.Access] = [];
          collection[e.data.properties.Access].push({
            data: e.data,
            group: e.group,
            classes: e.classes
          });
        });

        let actions = JSON.parse(JSON.stringify(edges.jsons()[0]));
        actions.data.id = `c${source}${target}`;
        actions.data.name = `${edges.length} Actions`;
        actions.data["collection"] = collection;
        actions.classes = ["ACTIONS"].concat(Object.keys(collection));
        add.push(actions);
        remove.push.apply(remove, edges);
      });

      cy.zoomingEnabled(false);
      this.remove_element(remove);
      this.add_element(add);
      cy.zoomingEnabled(true);
    },

    expand_actions(element) {
      let collection = element.data("collection");
      cy.zoomingEnabled(false);
      cy.elements().lock();
      this.add_element(
        Object.keys(collection)
          .map(k => collection[k])
          .flat()
      );
      this.remove_element(element);
      cy.elements().unlock();
      cy.zoomingEnabled(true);
    },

    expand_collapse(element) {
      this.loading.enabled = false;

      if (element.hasClass("expanded")) {
        let nodes = cy
          .elements()
          .filter(`#${element.data("id")}`)
          .connectedEdges()
          .connectedNodes()
          .filter(`[[degree = 1]][id != '${element.data("id")}']`);

        let edges = cy
          .elements()
          .filter(`#${element.data("id")}`)
          .edgesWith(nodes);

        let elements = nodes.union(edges);
        element.data("elements", elements.jsons());

        if (elements.length > 0) {
          this.remove_element(elements);
          element.removeClass("expanded");
          element.addClass("collapsed");
        }
      } else if (
        element.hasClass("collapsed") &&
        element.data("elements").length > 0
      ) {
        this.add_element(element.data("elements"));
        element.removeClass("collapsed");
        element.addClass("expanded");
      } else {
        element.addClass("collapsed");

        const id = (typeof element.data == "function"
          ? element.data().id
          : element.data.id
        ).substring(1);

        this.query(
          `MATCH (source) WHERE ID(source) = ${id} ` +
            `OPTIONAL MATCH path=(source)-[:TRANSITIVE|ASSOCIATIVE]-() ` +
            "RETURN source, path"
        )
          .then(elements => {
            let collection = cytoscape().collection(elements);
            collection = collection.difference(cy.elements());
            element.data("elements", collection);
            this.add_element(element.data("elements"));
            element.removeClass("collapsed");
            element.addClass("expanded");
            this.loading.enabled = true;
          })
          .finally(() => {
            this.loading.enabled = true;
          });
      }
    },

    add_element(elements) {
      let collection = "length" in elements ? elements : [elements];

      if (collection.length < 1) return collection;

      // TODO: filter for duplicate actions (collapsed vs uncollapsed).

      if (collection.length < this.limit.threshold) {
        return this.add_element_continue(collection);
      }

      this.add_element_pause(collection);
    },

    add_element_pause(collection) {
      this.limit.display = true;
      this.limit.elements = collection;
      this.limit.size = collection.length;
    },

    add_element_continue(collection) {
      this.limit.display = false;
      this.limit.elements = [];
      this.loading.graph = true;
      this.destroy_menu();

      let elements = cy.add(collection);
      cy.elements()
        .makeLayout({
          ...config.graph.layout
        })
        .run();
      this.loading.graph = false;
      return elements;
    },

    remove_element(elements) {
      const that = this;

      let remove = cy.collection();
      let collection = "length" in elements ? elements : [elements];

      if (collection.length < 1) return false;

      this.loading.graph = true;
      this.destroy_menu();

      collection = collection.map(e => {
        let id = (typeof e.data !== "function"
          ? cy.elements().$id(e.data.id)
          : e
        ).data("id");
        remove.merge(cy.filter(`#${id}`));
      });

      remove.merge(cy.elements("node").edgesWith(remove));

      this.loading.graph = false;
      remove.animate({
        style: {
          opacity: "0",
          "background-color": "Red",
          "line-color": "Red"
        },
        duration: 250,
        complete: function() {
          cy.remove(remove);
          that.elements = cy
            .elements("node")
            .map(n => n.data("properties").Arn);
        }
      });
      return true;
    },

    query(query, loader = true) {
      const that = this;
      let results = [];
      let elements = {};

      this.limit.query = query;

      function add_node(__node) {
        let node = {};
        let id = "n" + __node.identity.toString();

        if (id in elements) return elements[id];

        node.group = "nodes";
        node.classes = __node.labels.join(" ").replace(/::/g, " ");
        node.scratch = {};
        node.data = {
          id: id,
          name: __node.properties.Name,
          properties: __node.properties,
          type: __node.labels.filter(
            c =>
              !["Resource", "Pattern", "Generic", "Admin", "External"].includes(
                c
              )
          )[0]
        };

        elements[id] = node;

        return elements[id];
      }

      function add_edge(__edge) {
        let edge = {};
        let source = "n" + __edge.relationship.start.toString();
        let target = "n" + __edge.relationship.end.toString();
        let id = "e" + __edge.relationship.identity.toString();

        add_node(__edge.start);
        add_node(__edge.end);

        edge.group = "edges";
        edge.classes = __edge.relationship.type;
        (edge.scratch = {}),
          (edge.data = {
            id: id,
            name: __edge.relationship.properties.Name,
            source: source,
            target: target,
            properties: __edge.relationship.properties
          });

        elements[id] = edge;

        return [elements[source], elements[target], elements[id]];
      }

      function typecast(result) {
        if (result == null || typeof result === "number") return result;
        // Node
        else if (typeof result == "object" && "labels" in result)
          return add_node(result);
        // Path
        else if (
          typeof result === "object" &&
          "segments" in result &&
          result.segments.length > 0
        )
          return result.segments.map(segment => {
            return add_edge(segment);
          });
        // Boolean
        else if (
          typeof result === "boolean" ||
          result.toString().toLowerCase() == "true" ||
          result.toString().toLowerCase() == "false"
        )
          return result.toString().toLowerCase() === "true";
        // Integer
        else if (
          typeof result === "object" &&
          Object.keys(result).includes("high") &&
          Object.keys(result).includes("low")
        )
          return parseInt(result.toString());

        // String
        if (typeof result === "string") return result.toString();
        // Array
        else if (Array.isArray(result)) return result.map(e => typecast(e));
        else if (typeof result === "object") {
          Object.keys(result).map(k => (result[k] = typecast(result[k])));
          return result;
        }

        // Unknown
        //else console.log(result, "is of an unknown type");
        return null;
      }

      function format(elements) {
        let __action_count = 0;
        let __elements = [];
        let __actions = {};

        elements.forEach(function(node) {
          if (
            node.classes.indexOf("Resource") != -1 ||
            node.classes.indexOf("Generic") != -1 ||
            node.classes.indexOf("External") != -1
          )
            __elements.unshift(node);
          else if (
            node.classes.indexOf("TRANSITIVE") != -1 ||
            node.classes.indexOf("ASSOCIATIVE") != -1
          )
            __elements.push(node);
          else if (node.classes.indexOf("ACTION") != -1) {
            node.classes += ` ${node.data.properties.Effect}`;
            node.classes += ` ${node.data.properties.Access.replace(" ", "")}`;
            if ("Condition" in node.data.properties) {
              if (
                typeof node.data.properties.Condition === "string" &&
                node.data.properties.Condition !== "[]"
              )
                node.classes += " Conditional";
              else delete node.data.properties.Condition;
            }

            if (!(node.data.source in __actions))
              __actions[node.data.source] = {};

            if (!(node.data.target in __actions[node.data.source])) {
              __actions[node.data.source][node.data.target] = {
                group: "edges",
                scratch: {},
                data: {
                  name: "Actions",
                  id: node.data.id.replace("e", "c"),
                  source: node.data.source,
                  target: node.data.target
                }
              };
              __actions[node.data.source][
                node.data.target
              ].data.collection = {};
            }

            const collection =
              __actions[node.data.source][node.data.target].data.collection;
            if (!(node.data.properties.Access in collection))
              collection[node.data.properties.Access] = [];

            let action = {
              data: node.data,
              group: node.group,
              classes: ["ACTION", node.data.properties.Access]
            };

            if (Object.keys(node.data.properties).includes("Condition"))
              action.classes.push("Conditional");

            collection[node.data.properties.Access].push(action);
            __action_count += 1;
          } else if (node.classes.indexOf("Admin") != -1) {
            __elements.unshift(node);

            elements
              .filter(
                n => n.data.target != null && n.data.target === node.data.id
              )
              .forEach(function(e) {
                e.classes = "ATTACK";
                __elements.push(e);
              });
          } else if (node.classes.indexOf("Pattern") != -1) {
            var source_edge = {};
            var target_edges = [];
            var option_edges = [];

            source_edge = elements.find(
              n => n.data.target != null && n.data.target === node.data.id
            );

            for (var i = 0; i < elements.length; i++) {
              var n = elements[i];

              if (n.group != "edges") continue;

              if (
                n.classes.indexOf("ATTACK") != -1 &&
                n.data.source == node.data.id
              ) {
                target_edges.push(n);
              } else if (
                n.classes.indexOf("OPTION") != -1 &&
                n.data.source == node.data.id
              )
                option_edges.push(n);
            }

            target_edges.forEach(function(e) {
              e.classes = "ATTACK";
              e.data.source = source_edge.data.source;
              e.data.options = option_edges;
              __elements.push(e);
            });
          }
        });

        // Post process actions:

        Object.keys(__actions).map(k => {
          Object.keys(__actions[k]).map(v => {
            const collection = Object.keys(__actions[k][v].data.collection)
              .map(c => __actions[k][v].data.collection[c])
              .flat();
            // Group actions if there are more than 'x' in the result set
            // or if there are more than 'y' between two nodes (directed).
            if (true && (__action_count > 200 || collection.length > 20)) {
              __actions[k][v].data.name = `${collection.length} Actions`;
              __actions[k][v].data.id = `c${k}${v}`;
              __actions[k][v].classes = ["ACTIONS"].concat(
                Object.keys(__actions[k][v].data.collection)
              );
              __elements.push(__actions[k][v]);
            } else {
              __elements.push.apply(__elements, collection);
            }
          });
        });

        let collection = cytoscape({ elements: __elements }).elements();

        // Collapse nodes with an indegree > 10

        let exclude = [];

        collection.filter("[[indegree > 10]]").map(e => {
          // Skip nodes that are in the process of being expanded
          if (cy.filter(`#${e.data("id")}`).some(n => n.hasClass("collapsed")))
            return false;

          let nodes = e
            .connectedEdges(`edge.TRANSITIVE[target = "${e.data("id")}"]`)
            .connectedNodes()
            .filter("[[degree = 1]]")
            .filter(`[id != '${e.data("id")}']`);

          let edges = collection.filter(`#${e.data("id")}`).edgesWith(nodes);

          e.data("elements", []);
          e.addClass("collapsed");

          exclude.push.apply(
            exclude,
            nodes
              .union(edges)
              .jsons()
              .map(n => n.data.id)
          );
        });

        return collection
          .filter(e => {
            return !exclude.includes(e.data("id"));
          })
          .jsons();
      }

      if (loader) this.loading.query = true;
      const neo4j = this.$neo4j.session();

      return neo4j
        .run(query)
        .then(response => {
          if (response.records.length <= 0) return [];

          response.records.forEach(function(record) {
            let result = {};
            for (var i = 0; i < record._fields.length; i++) {
              result[record.keys[i]] = typecast(record._fields[i]);
            }
            results.push(result);
          });

          if (Object.keys(elements).length === 0) return results;
          else return format(Object.keys(elements).map(k => elements[k]));
        })
        .catch(e => {
          this.message.color = "error";
          this.message.text = e;
          this.message.visible = true;
          console.log("[ERR]:", e);
        })
        .finally(() => {
          neo4j.close();
          if (loader) this.loading.query = false;
        });
    },

    create_menu(element) {
      if (element.isNode != null && element.isNode()) {
        this.events.menu = {
          id: element.id(),
          enabled: true
        };

        element.removeClass("hover");
        element.addClass("menu");
        cy.autoungrabify(true);
        cy.autounselectify(true);
        cy.zoomingEnabled(false);
        cy.panningEnabled(false);
      }
    },

    destroy_menu() {
      if (this.events.menu.enabled) {
        const node = cy.$(`#${this.events.menu.id}`);
        this.events.menu = {
          enabled: false
        };

        node.removeClass("menu");
        cy.autoungrabify(false);
        cy.autounselectify(false);
        cy.zoomingEnabled(true);
        cy.panningEnabled(true);
      }
    },

    button(fn, target) {
      this.destroy_menu();
      this.hide = true;
      fn(target).then(elements => {
        if (!Array.isArray(elements) || elements.length === 0) return;
        const added = this.add_element(elements);
        // if (added.length > 0) {
        //   this.message.text = `Added ${added.length} elements!`;
        //   this.message.color = "success";
        //   this.message.visible = true;
        // }
      });
    },

    register_listeners() {
      window.addEventListener("keydown", event => {
        switch (event.key) {
          case "Tab":
            event.preventDefault();
            this.hide = false;
            this.events.alt = !this.events.alt;

            break;
          case "Control":
            event.preventDefault();
            this.events.ctrl = true;
            break;
          case "a":
            if (event.ctrlKey) {
              event.preventDefault();
              cy.elements().removeClass("unselected");
              cy.elements().addClass("selected");
            }
            break;
          case "s":
            if (event.ctrlKey) {
              event.preventDefault();
              this.hide = false;
            }
            break;
          // TODO: add 'Up' and 'Down' arrow keys to move node(s)
          // case "h":
          //   event.preventDefault();
          //   if (event.ctrlKey) {
          //   }
          //   break;
          case "default":
            this.events.ctrl = event.ctrlKey;
            break;
        }
      });

      // Keyboard events
      window.addEventListener("keyup", event => {
        switch (event.key) {
          case "Control":
            event.preventDefault();
            this.events.ctrl = false;
            break;
          case "c":
            if (event.ctrlKey) {
              const clipboard = JSON.stringify(
                cy.elements("node.selected").map(e => {
                  return e.data("properties");
                })
              );
              navigator.clipboard.writeText(clipboard);
            }
            break;
          case "Delete":
            this.remove_element(cy.elements(".selected"));
            break;
          case "Escape":
            this.element_properties = null;
            this.hide = true;
            break;
          case "Enter":
            if (event.altKey) {
              // this.collapse_actions_all();
              cy.elements()
                .makeLayout({
                  ...config.graph.layout
                })
                .run();
            }
            break;
          default:
            break;
        }
      });

      cy.on("boxselect", event => {
        event.target.addClass("selected");
        event.target.removeClass("unselected");
      });

      cy.on("mouseover", event => {
        if (event.target.addClass != null) event.target.addClass("hover");
      });

      cy.on("mouseout", event => {
        if (event.target.removeClass != null) event.target.removeClass("hover");
      });

      cy.on("cxttap", "node", event => {
        this.hide = true;
        this.create_menu(event.target);
      });

      cy.on("click", event => {
        const timeout = 350;
        const click = {
          id: event.target.data("id"),
          time: event.timeStamp,
          timeout: null
        };

        if (!event.target.id) {
          event.target.trigger("singleclick");
          return;
        }

        if (
          click.id === this.events.select.id &&
          click.time - this.events.select.time < timeout
        ) {
          clearTimeout(this.events.select.timeout);
          event.target.trigger("doubleclick");
        } else {
          if (this.events.select.timeout)
            clearTimeout(this.events.select.timeout);

          this.events.select = click;
          this.events.select.timeout = setTimeout(() => {
            event.target.trigger("singleclick");
          }, timeout);
        }
      });

      cy.on("doubleclick", "node", event => {
        this.expand_collapse(event.target);
      });

      cy.on("doubleclick", "edge.ACTIONS", event => {
        this.expand_actions(event.target);
      });

      cy.on("doubleclick", "edge.ACTION", event => {
        this.collapse_actions(event.target);
      });

      cy.on("singleclick", event => {
        this.hide = true;
        this.destroy_menu();

        if (event.target.group) {
          let collection = cy.collection();

          if (!this.events.ctrl) {
            if (event.target.group() == "nodes") {
              let edges = event.target.edgesTo("node");
              let nodes = edges.connectedNodes();
              collection.merge(event.target);
              collection.merge(edges);
              collection.merge(nodes);
            } else if (event.target.group() == "edges") {
              collection.merge(event.target.connectedNodes());
              collection.merge(event.target);
            }
            cy.elements().addClass("unselected");
            cy.elements(".selected").removeClass("selected");

            event.target.addClass("selected");
            collection.removeClass("unselected");
            this.element_properties = event.target.json();
          } else {
            event.target.removeClass("unselected");

            if (event.target.hasClass("selected")) {
              event.target.removeClass("selected");
            } else {
              event.target.addClass("selected");
            }
          }
        } else if (!this.events.ctrl) {
          this.element_properties = null;
          cy.elements(".unselected").removeClass("unselected");
          cy.elements(".selected").removeClass("selected");
        }
      });
    }
  },

  mounted() {
    cytoscape.use(dagre);

    cy = cytoscape({
      container: document.getElementsByClassName("graph")[0],
      elements: config.elements,
      style: config.graph.style,
      layout: config.graph.layout,
      wheelSensitivity: 0.1,
      maxZoom: 1.5,
      minZoom: 0.2
    });

    cy.boxSelectionEnabled(true);
    this.register_listeners();
  },

  computed: {
    menu: function() {
      if (Object.keys(this.events.menu).length == 0) return {};
      if (!this.events.menu.enabled) return {};

      const br = 28;
      const bl = 60;
      const bm = 1.6;

      const node = cy.$(`#${this.events.menu.id}`);
      const theta = (2 * Math.PI) / this.buttons.length;

      const offset =
        this.buttons.length % 2 == 0 ? 0 : (Math.PI / 2) * this.buttons.length;

      let r = bm * (node.style("height").replace("px", "") / 2) * cy.zoom();
      let position = node.renderedPosition();

      r = r < bl ? bl : r;
      position.x -= br;
      position.y -= br;

      for (let i = 0; i < this.buttons.length; i++) {
        const x = position.x + r * Math.cos(i * theta - offset);
        const y = position.y + r * Math.sin(i * theta - offset);

        this.buttons[i].target = node;
        this.buttons[i].position = {
          x: x + "px",
          y: y + "px"
        };
      }

      return this.buttons;
    },
    busy: function() {
      return this.loading.enabled && (this.loading.query || this.loading.graph);
    }
  }
};
</script>

<style>
.v-application {
  font-family: "Source Code Pro" !important;
  font-size: 14px !important;
}

#graph {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: absolute;
  z-index: 0;
}

.graph canvas {
  left: 0px !important;
}
</style>

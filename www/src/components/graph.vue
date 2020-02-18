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

    <!-- Node context menu -->
    <v-fab-transition
      transition="scale-transition"
      v-for="(item,i) in context_menu"
      :key="'context_menu-' + i"
    >
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            :style="context_menu[i].styles.button"
            :height="context_menu[i].styles.size"
            :width="context_menu[i].styles.size"
            @click="context_menu_item(item.fn, item.target)"
            absolute
            fab
            dark
            v-on="on"
          >
            <v-icon
              :style="context_menu[i].styles.icon"
              :size="context_menu[i].styles.icon.width"
            >{{item.icon}}</v-icon>
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
        context_menu: {},
        select: {},
        alt: false,
        ctrl: false
      },
      elements: [],
      hide: false,
      element_properties: null,
      context_menu_items: [
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
    context_menu_item(fn, target) {
      this.context_menu_destroy();
      this.hide = true;
      fn(target).then(response => {
        const elements = response.Graph;
        if (typeof elements === "undefined" || elements.length === 0) return;
        const added = this.add_element(elements);
        if (added.length > 0) {
          // this.message.text = `Added ${added.length} elements!`;
          // this.message.color = "success";
          // this.message.visible = true;
        }
      });
    },

    context_menu_create(element) {
      if (element.isNode != null && element.isNode()) {
        this.events.context_menu = {
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

    context_menu_destroy() {
      if (this.events.context_menu.enabled) {
        const node = cy.$(`#${this.events.context_menu.id}`);
        this.events.context_menu = {
          enabled: false
        };

        node.removeClass("menu");
        cy.autoungrabify(false);
        cy.autounselectify(false);
        cy.zoomingEnabled(true);
        cy.panningEnabled(true);
      }
    },

    show() {
      this.hide = !this.hide;
    },

    find_paths_to(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);

      return this.neo4j.run(
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
      return this.neo4j.run(
        `MATCH (source) WHERE ID(source) = ${id} ` +
          "OPTIONAL MATCH path=shortestPath((source)-[:TRANSITIVE|ATTACK*0..]->(target)) " +
          "WHERE (target:Resource OR target:Admin) " +
          "AND source <> target " +
          "RETURN source, path"
      );
    },

    find_actions(actions) {
      this.neo4j
        .run(
          `WITH "${actions}" AS action ` +
            "MATCH path=()-[:ACTION{Name:action}]->() RETURN path"
        )
        .then(elements => {
          this.add_element(elements.Graph);
        });
    },

    find_actions_to(element) {
      const id = (typeof element.data == "function"
        ? element.data().id
        : element.data.id
      ).substring(1);

      return this.neo4j.run(
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

      return this.neo4j.run(
        `MATCH (source) WHERE ID(source) = ${id} ` +
          "OPTIONAL MATCH actions=(source)-[:ACTION]->(:Resource) " +
          "RETURN source, actions"
      );
    },

    bundle_actions_all() {
      let elements = [];
      let actions = {};
      cy.edges((e, i) => e.hasClass("ACTION")).map(a => {
        if (!(a.data("source") in actions)) actions[a.data("source")] = [];
        if (!(a.data("target") in actions[a.data("source")])) {
          actions[a.data("source")].push(a.data("target"));
          elements.push(a);
        }
      });
      this.bundle_actions(elements);
    },

    bundle_actions(elements) {
      let collections = {};
      let remove = [];
      let add = [];

      remove = cy.edges().filter(e => {
        if (
          e.hasClass("ACTION") &&
          elements.every(
            element =>
              e.data("source") === element.data("source") &&
              e.data("target") === element.data("target")
          )
        ) {
          const id = `${e.data("source")}-${e.data("target")}`;
          const access = e.data("properties").Access;
          if (!(id in collections)) collections[id] = {};
          if (!(access in collections[id])) collections[id][access] = [];
          collections[id][access].push(e.json());
          return true;
        }
        return false;
      });

      Object.keys(collections).forEach(k => {
        const actions = Object.keys(collections[k])
          .map(a => collections[k][a])
          .flat();

        add.push({
          classes: ["ACTIONS"].concat(
            Array.from(new Set(actions.map(a => a.data.properties.Effect)))
          ),
          data: {
            id: `c${actions
              .map(a => parseInt(a.data.id.replace("e", "")))
              .reduce((a, b) => a + b)}`,
            name: actions.length > 1 ? `${actions.length} Actions` : `1 Action`,
            source: actions[0].data.source,
            target: actions[0].data.target,
            properties: collections[k]
          }
        });
      });

      cy.zoomingEnabled(false);
      this.remove_element(remove).then(() => this.add_element(add));
      cy.zoomingEnabled(true);
    },

    unbundle_actions(element) {
      let collection = element.data("properties");
      cy.zoomingEnabled(false);
      cy.elements().lock();
      this.remove_element(element);

      this.add_element(
        Object.keys(collection)
          .map(k => collection[k])
          .flat()
      );

      cy.elements().unlock();
      cy.zoomingEnabled(true);
    },

    expand_collapse(element) {
      const that = this;

      function _expand(element) {
        that.loading.enabled = false;
        const id = (typeof element.data == "function"
          ? element.data().id
          : element.data.id
        ).substring(1);

        that.neo4j
          .run(
            `MATCH (source) WHERE ID(source) = ${id} ` +
              `OPTIONAL MATCH path=(source)-[:TRANSITIVE|ASSOCIATIVE]-() ` +
              "RETURN source, path"
          )
          .then(elements => {
            that.loading.enabled = true;

            element.removeClass("expandible");

            let collection = cytoscape().collection(elements.Graph);
            collection = collection.difference(cy.elements());

            if (that.add_element(collection).length > 0)
              element.addClass("collapsible");
            else element.addClass("unexpandible");
          })
          .finally(() => {
            that.loading.enabled = true;
          });
      }

      function _collapse(element) {
        element.removeClass("collapsible");
        // Removes all derivative nodes (:ANY to element, ASSOCIATIVE to|from element)
        let nodes = cy
          .elements()
          .filter(`#${element.data("id")}`)
          .connectedEdges()
          .filter(e => e.hasClass("ASSOCIATIVE") || e.hasClass("TRANSITIVE"))
          .connectedNodes()
          .filter(`[[degree = 1]][id != '${element.data("id")}']`);

        let edges = cy
          .elements()
          .filter(`#${element.data("id")}`)
          .edgesWith(nodes);

        let elements = nodes.union(edges);

        if (elements.length > 0) {
          that.remove_element(elements);
          element.removeClass("unexpandible");
          element.addClass("expandible");
        }
      }

      if (element.hasClass("collapsible") || element.hasClass("unexpandible")) {
        _collapse(element);
      } else {
        _expand(element);
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
      this.context_menu_destroy();

      let elements = cy.add(collection);
      const concentric = cy
        .edges()
        .map(e => [e.data("source"), e.data("target")])
        .reduce((v, e, i) => {
          if (i === 0) return e;
          else return v.filter(x => e.includes(x));
        }, []);

      const layout =
        cy.elements().filter("edge").length === 0
          ? // Set 'grid' layout when there are no edges
            {
              name: "grid",
              rows: Math.ceil(cy.nodes().length / 10),
              avoidOverlap: true,
              avoidOverlapPadding: 20,
              nodeDimensionsIncludeLabels: true
            }
          : concentric.length > 0
          ? // Set 'concentric' layout when the graph consists of
            // one node connected to every other node
            {
              name: "concentric",
              minNodeSpacing: 50,
              concentric: n => {
                return concentric.includes(n.data("id")) ? n.degree() : 1;
              },
              spacingFactor: Math.max(10 / cy.elements().nodes().length, 1),
              startAngle: 0,
              fit: true
            }
          : // Otherwise set default (dagre)
            config.graph.layout;

      cy.elements()
        .makeLayout({
          ...layout,
          animate: true
        })
        .run()
        .promiseOn("layoutstop", () => {});
      this.loading.graph = false;
      return elements;
    },

    remove_element(elements) {
      const that = this;

      let remove = cy.collection();
      let collection = "length" in elements ? elements : [elements];

      if (collection.length < 1) return false;

      this.loading.value = true;
      this.context_menu_destroy();

      collection = collection.map(e => {
        let id = (typeof e.data !== "function"
          ? cy.elements().$id(e.data.id)
          : e
        ).data("id");
        remove.merge(cy.filter(`#${id}`));
      });

      remove.merge(cy.elements("node").edgesWith(remove));

      this.loading.value = false;

      return new Promise((resolve, reject) => {
        // TODO: Animation bug, promise resolves prematurely

        // remove.animate({
        //   style: {
        //     opacity: "0",
        //     "background-color": "Red",
        //     "line-color": "Red"
        //   },
        //   duration: 250,
        //   complete: function() {
        //     cy.remove(remove);
        //     resolve();
        //   }
        // });

        cy.remove(remove);
        resolve();
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
              // this.bundle_actions_all();
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
        this.context_menu_create(event.target);
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
        this.unbundle_actions(event.target);
      });

      cy.on("doubleclick", "edge.ACTION", event => {
        this.bundle_actions(event.target);
      });

      cy.on("singleclick", event => {
        this.hide = true;
        this.context_menu_destroy();

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

  watch: {
    db_error() {}
  },

  computed: {
    db_error: function() {
      const message =
        typeof this.neo4j.error.message === "string"
          ? this.neo4j.error.message
          : "";
      if (message === "") return;

      this.message.text = message;
      this.message.color = "error";
      this.message.visible = true;
    },

    context_menu: function() {
      if (Object.keys(this.events.context_menu).length == 0) return {};
      if (!this.events.context_menu.enabled) return {};

      const theta = (2 * Math.PI) / this.context_menu_items.length;
      const delta =
        this.context_menu_items.length % 2 == 0
          ? 0
          : (Math.PI / 2) * this.context_menu_items.length;

      const node = cy.$(`#${this.events.context_menu.id}`);
      let position = node.renderedPosition();

      let r =
        (1.1 /*radius scaling factor*/ *
        cy.zoom() *
        0.75 /*zoom dampener */ *
          parseFloat(node.style("height").replace("px", ""))) /
        1.5; /*hover size multiplier*/

      // button size is relative to node size
      let button_size = (3 / 4) * r;
      // account for button size when computing context menu radius
      r += button_size / 2;

      for (let i = 0; i < this.context_menu_items.length; i++) {
        const x = r * Math.cos(i * theta - delta);
        const y = r * Math.sin(i * theta - delta);
        this.context_menu_items[i].target = node;
        this.context_menu_items[i].styles = {
          button: {
            top: position.y + y - button_size / 2 + "px",
            left: position.x + x - button_size / 2 + "px"
          },
          icon: {
            height: button_size / 2 + "px",
            width: button_size / 2 + "px"
          },
          size: button_size
        };
      }

      return this.context_menu_items;
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

<template>
  <div>
    <!-- Success notifications - timeout -->
    <v-snackbar
      v-if="notification.status === 0"
      v-model="notification.visible"
      :timeout="1000"
      color="success"
      class="notice"
      top
    >
      <span class="mx-auto" v-html="notification.text"></span>
    </v-snackbar>

    <!-- Errors - dismissible, no timeout -->
    <v-alert
      v-else-if="notification.status === 1"
      v-model="notification.visible"
      class="mx-auto notification notice"
      type="error"
      dismissible
    >
      <span v-html="notification.text"></span>
    </v-alert>

    <!-- Confirmation dialog -->
    <v-dialog class="notice" max-width="550" modal v-model="dialog.enabled">
      <v-card>
        <v-card-title class="headline py-5">Hold up</v-card-title>

        <v-card-text class="text-md-left">
          You're about to draw
          <b>{{dialog.store.length}}</b> nodes and edges, which is probably not a great idea.
          <br />
          <br />Consider refining your search or limiting the result set to text-based output only.
          <br />
          <br />As a starting point, the query that was issued was:
          <br />
          <br />
          <b>{{neo4j.state.statement}}</b>
        </v-card-text>

        <v-card-actions>
          <v-btn outlined color="green darken-1" @click="dialog.enabled = false" text>Cancel</v-btn>
          <v-btn color="red darken-1" text @click="_add_resume(dialog.store)">Roll the dice!</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Progress overlay -->
    <v-overlay :value="busy" class="notice">
      <v-progress-circular :size="200" :width="8" indeterminate color="primary"></v-progress-circular>
    </v-overlay>

    <!-- Database connection helper -->
    <Database
      ref="database"
      @resources="database.resources = $event"
      @actions="database.actions = $event"
      :enable="database.enable"
    />

    <!-- Graph -->
    <v-card flat tile append :disabled="busy" class="graph" id="graph" />

    <!-- Navigation drawer (Right hand side) -->
    <Menu
      @redact="menu_redact"
      @screenshot="menu_screenshot"
      @load="menu_load_saved_queries"
      @update_layout="menu_update_layout"
      @database="$refs.database.db_settings_open()"
      @clear="clear"
    ></Menu>

    <!-- Node context menu -->
    <v-fab-transition
      transition="scale-transition"
      v-for="(item,i) in context_menu"
      :key="'context_menu-' + i"
    >
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            v-on="on"
            @click="context_menu_item(item.fn, item.target)"
            :style="context_menu[i].styles.button"
            :height="context_menu[i].styles.size"
            :width="context_menu[i].styles.size"
            absolute
            dark
            fab
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

    <!-- Element properties pane (left hand side) -->
    <Properties v-show="properties.enabled" :properties="properties.value"></Properties>

    <!-- Search bar (bottom) -->
    <Search
      v-show="search.enabled"
      ref="search"
      @add="add"
      @clear="clear"
      @show="search.visible = $event"
      @advanced="search.advanced = $event"
      @visual_queries_active="search.visual_queries_active = $event"
      :visual_queries_active="search.visual_queries_active"
      :show="search.visible"
      :resources="database.resources"
      :actions="database.actions"
      :advanced="search.advanced"
    ></Search>
  </div>
</template>

<script>
import Properties from "@/components/Properties";
import Database from "@/components/Database";
import Search from "@/components/Search";
import Menu from "@/components/Menu";

import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import config from "@/config.js";

let cy = null;

export default {
  name: "Graph",
  components: { Properties, Database, Search, Menu },

  data: function() {
    return {
      database: {
        actions: [],
        resources: [],
        enabled: true
      },
      notification: {
        text: "",
        status: 0,
        visible: false
      },
      loading: {
        value: false,
        enabled: true
      },
      properties: {
        value: null,
        enabled: true
      },
      search: {
        visible: true,
        enabled: true,
        advanced: false,
        visual_queries_active: false
      },
      context_menu_items: [
        {
          name: "Outbound <b>Paths</b>",
          icon: "mdi-map-marker-outline",
          fn: this.find_paths_from
        },
        {
          name: "Outbound <b>Actions</b>",
          icon: "mdi-chevron-right-circle-outline",
          fn: this.find_actions_from
        },
        {
          name: "Inbound <b>Paths</b>",
          icon: "mdi-map-marker",
          fn: this.find_paths_to
        },
        {
          name: "Inbound <b>Actions</b>",
          icon: "mdi-chevron-right-circle",
          fn: this.find_actions_to
        }
      ],
      events: {
        clicked: {},
        context_menu: {}
      },
      dialog: {
        max_elements: 500,
        enabled: false,
        store: []
      },
      layout: {
        name: "Auto"
      }
    };
  },

  methods: {
    context_menu_create(element) {
      if (element.isNode != null && element.isNode()) {
        this.events.context_menu = {
          id: element.id(),
          enabled: true
        };

        element.removeClass("hover");
        element.addClass("context-menu");
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

        node.removeClass("context-menu");
        cy.autoungrabify(false);
        cy.autounselectify(false);
        cy.zoomingEnabled(true);
        cy.panningEnabled(true);
      }
    },

    context_menu_item(fn, target) {
      this.context_menu_destroy();
      this.search.visible = false;
      fn(target).then(response => {
        const elements = response.Graph;
        if (typeof elements === "undefined" || elements.length === 0) return;
        const added = this.add(elements);
        if (added.length > 0) {
          // this.notification.text = `Added ${added.length} elements!`;
          // this.notification.status = 0;
          // this.notification.visible = true;
        }
      });
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
          "OPTIONAL MATCH actions=(source)-[:ACTION]->(target) " +
          "WHERE target:Resource OR target:CatchAll " +
          "RETURN source, actions"
      );
    },

    unbundle_actions(element) {
      let collection = element.data("properties");
      cy.zoomingEnabled(false);
      cy.elements().lock();
      this.remove(element);

      this.add(
        Object.keys(collection)
          .map(k => collection[k])
          .flat()
      );

      cy.elements().unlock();
      cy.zoomingEnabled(true);
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
      this.remove(remove).then(() => this.add(add));
      cy.zoomingEnabled(true);
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

            if (that.add(collection).length > 0)
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
          that.remove(elements);
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

    add(elements) {
      let collection = "length" in elements ? elements : [elements];
      if (collection.length < 1) return collection;

      if (collection.length < this.dialog.max_elements) {
        return this._add_resume(collection);
      }
      return this._add_suspend(collection);
    },

    _add_suspend(collection) {
      this.dialog.enabled = true;
      this.dialog.store = collection;
      return [];
    },

    _add_merge_actions(collection) {
      cy.startBatch();
      const merged = collection
        .map(c => (typeof c.data === "function" ? c.json() : c))
        .filter(e => {
          if (!(e.classes.includes("ACTION") || e.classes.includes("ACTIONS")))
            return true;

          const existing = cy
            .edges()
            .filter(
              a =>
                a.data("id") !== e.data.id &&
                !a.removed() &&
                (a.hasClass("ACTION") || a.hasClass("ACTIONS")) &&
                a.data("source") === e.data.source &&
                a.data("target") === e.data.target
            );

          // No existing action(s), add them all
          if (existing.length === 0) return true;

          let bundle = null;
          const new_action = e.classes.includes("ACTION") ? [e] : [];
          const new_actions = e.classes.includes("ACTIONS") ? [e] : [];
          let actions = existing.filter(a => a.hasClass("ACTION"));
          let bundles = existing.filter(a => a.hasClass("ACTIONS"));

          if (bundles.length === 0) {
            // We need to modify an action to create a bundle
            const action = actions[0].json();
            bundle = actions[0];
            bundle.classes().map(c => bundle.removeClass(c));
            bundle
              .addClass("ACTIONS")
              .addClass(bundle.data("properties").Effect);

            bundle.data("properties", {
              [bundle.data("properties").Access]: [action]
            });
            bundle.data("type", "ACTIONS");

            actions = actions.filter(
              a => a.data("id") !== actions[0].data("id")
            );

            bundle = cy.remove(bundle).json();
            bundle = cy.add({
              ...bundle,
              data: {
                ...bundle.data,
                id: `a${bundle.data.source}-${bundle.data.target}`
              }
            });
          } else {
            // We can use an existing bundle
            bundle = bundles[0];
            bundles = bundles.filter(
              a => a.data("id") !== bundles[0].data("id")
            );
          }

          // Add actions to bundle
          bundles
            .jsons()
            .concat(new_actions)
            .map(b =>
              Object.keys(b.data.properties)
                .map(k => b.data.properties[k])
                .flat()
            )
            .flat()
            .concat(actions.jsons())
            .concat(new_action)
            .map(a => {
              if (!(a.data.properties.Access in bundle.data("properties")))
                bundle.data("properties")[a.data.properties.Access] = [];
              if (
                !bundle
                  .data("properties")
                  [a.data.properties.Access].map(x => x.data.id)
                  .includes(a.data.id)
              ) {
                bundle.data("properties")[a.data.properties.Access].push(a);
              }
            });

          // Remove processed actions
          cy.remove(bundles);
          cy.remove(actions);

          actions = Object.keys(bundle.data("properties"))
            .map(k => bundle.data("properties")[k])
            .flat();

          // Update bundle properties
          bundle.data("name", `${actions.length} Actions`);
          bundle.classes().map(c => bundle.removeClass(c));
          Array.from(new Set(actions.map(a => a.data.properties.Effect)))
            .concat("ACTIONS")
            .map(c => bundle.addClass(c));

          return false;
        });
      cy.endBatch();
      return merged;
    },

    _add_resume(collection) {
      this.dialog.enabled = false;
      this.dialog.store = [];
      this.loading.value = true;
      this.context_menu_destroy();

      const elements = cy.add(this._add_merge_actions(collection));

      this.run_layout();
      return elements;
    },

    remove(elements) {
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

    clear() {
      return cy.elements().remove();
    },

    run_layout() {
      let layout = this.layout.name;
      let value = {};

      // Determine best fit for 'Auto'
      if (layout === "Auto") {
        const concentric = cy
          .edges()
          .map(e => [e.data("source"), e.data("target")])
          .reduce((v, e, i) => {
            return i === 0 ? e : v.filter(x => e.includes(x));
          }, []);

        // Set 'Grid' layout when there are no edges
        if (cy.elements().filter("edge").length === 0) layout = "Grid";
        // Set 'Concentric' layout when the graph consists of
        // one node connected to every other node
        else if (concentric.length > 0) layout = "Concentric";
        // Otherwise set 'Dagre'
        else layout = "Dagre";
      }

      switch (layout) {
        case "Concentric":
          // const degrees = cy.elements("node").reduce(
          //   (nodes, n) => ({
          //     ...nodes,
          //     [n.data("id")]: n.neighborhood("node").length
          //   }),
          //   {}
          // );

          value = {
            name: "concentric",
            minNodeSpacing: 50,
            boundingBox: undefined,
            spacingFactor: Math.max(20 / cy.elements("node").length, 1),
            startAngle: 0,
            // concentric: function(node) {
            //   return degrees[node.data("id")];
            // },
            fit: true
          };
          break;

        case "Grid":
          value = {
            name: "grid",
            avoidOverlap: true,
            avoidOverlapPadding: 20,
            nodeDimensionsIncludeLabels: true
          };
          break;

        default:
        case "Dagre":
          value = { ...config.graph.layout };
          break;
      }

      cy.elements()
        .makeLayout({
          ...value,
          animate: true
        })
        .run()
        .promiseOn("layoutstop", () => {});
      this.loading.value = false;
    },

    menu_redact: function(value) {
      let style = [];
      if (value)
        config.graph.style.map(s => {
          if (
            s.selector.includes("node") &&
            Object.keys(s.style).includes("label")
          ) {
            style.push({
              selector: s.selector,
              style: { label: "" }
            });
          }
        });
      this.properties.enabled = !value;
      this.search.enabled = !value;
      cy.style(config.graph.style.concat(style));
    },

    menu_screenshot() {
      const filename = `awspx_${new Date().getTime()}.png`;
      const png = cy.png({ bg: "white" });
      const download = document.createElement("a");
      download.href = png;
      download.download = filename;
      download.click();
    },

    menu_load_saved_queries() {
      this.search.visible = true;
      this.search.advanced = true;
      this.search.visual_queries_active = true;
    },

    menu_update_layout(value) {
      this.layout.name = value;
      this.run_layout();
    },

    register_listeners() {
      // Keyboard events
      window.addEventListener("keydown", event => {
        switch (event.key) {
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
              this.search.visible = true;
            }
            break;
          // TODO: Add panning using arrow keys
          case "default":
            break;
        }
      });

      window.addEventListener("keyup", event => {
        switch (event.key) {
          // TODO: Breaks clipboard, when copying foreground objects (eg policy documents)
          // case "c":
          //   if (event.ctrlKey) {
          //     const clipboard = JSON.stringify(
          //       cy.elements("node.selected").map(e => {
          //         return e.data("properties");
          //       })
          //     );
          //     navigator.clipboard.writeText(clipboard);
          //   }
          //   break;
          case "Delete":
            this.remove(cy.elements(".selected"));
            break;
          // case "Escape":
          //   this.properties.value = null;
          //   this.search.visible = false;
          //   break;
          case "Enter":
            if (event.altKey) {
              this.run_layout();
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
          event.target.trigger("singleclick", event);
          return;
        }

        if (
          click.id === this.events.clicked.id &&
          click.time - this.events.clicked.time < timeout
        ) {
          clearTimeout(this.events.clicked.timeout);
          event.target.trigger("doubleclick");
        } else {
          if (this.events.clicked.timeout)
            clearTimeout(this.events.clicked.timeout);

          this.events.clicked = click;
          this.events.clicked.timeout = setTimeout(() => {
            event.target.trigger("singleclick", event);
          }, timeout);
        }
      });

      cy.on("boxstart", event => {
        this.context_menu_destroy();
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

      cy.on("singleclick", (event, extra) => {
        this.search.visible = false;
        this.context_menu_destroy();
        const ctrl =
          typeof extra !== "undefined" ? extra.originalEvent.ctrlKey : false;

        if (event.target.group) {
          let collection = cy.collection();

          if (!ctrl) {
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
            cy.elements(".selected").removeClass("selected");
            cy.elements().addClass("unselected");
            collection.removeClass("unselected");
            event.target.addClass("selected");
            this.properties.value = event.target.json();
          } else {
            event.target.removeClass("unselected");

            if (event.target.hasClass("selected")) {
              event.target.removeClass("selected");
            } else {
              event.target.addClass("selected");
            }
          }
        } else if (!ctrl) {
          this.properties.value = null;
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
      wheelSensitivity: 0.1,
      maxZoom: 1.5,
      minZoom: 0.2
    });

    cy.boxSelectionEnabled(true);
    this.register_listeners();
  },

  watch: {
    db_error() {},
    "database.resources"() {
      this.clear();
      this.search.visible = true;
    }
  },

  computed: {
    db_error: function() {
      const message =
        typeof this.neo4j.error.message === "string"
          ? this.neo4j.error.message
          : "";

      this.notification.visible = false;
      if (message === "") return;

      this.notification.text = message
        .replace(/ /g, "&nbsp;")
        .replace(/\n/g, "<br>");
      this.notification.status = 1;
      this.notification.visible = true;
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
      return (
        this.loading.enabled &&
        (this.loading.value ||
          (this.database.resources.length > 0 && this.neo4j.state.active))
      );
    }
  }
};
</script>

<style>
#graph {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding-right: 60px;
  position: absolute;
  text-align: center;
  color: #2c3e50;
  z-index: 0;
  bottom: 0;
  right: 0;
  left: 0;
  top: 0;
}

.graph canvas {
  left: 0px !important;
}

.notice {
  z-index: 1000 !important;
}

.notification {
  position: absolute !important;
  max-width: 80% !important;
  transform: translateX(-50%);
  word-break: break-word;
  top: 5px !important;
  opacity: 1;
  z-index: 100;
  left: 50%;
}
</style>

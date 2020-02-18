<template>
  <div id="search">
    <v-expand-transition>
      <div v-if="show" class="mb-5">
        <v-card>
          <v-autocomplete
            :filter="filter"
            :items="(view == 0) ? resources : actions"
            :loading="loading"
            :cache-items="false"
            :aria-autocomplete="false"
            @update:search-input="update"
            v-model="selected"
            item-text="name"
            item-value="id"
            clearable
            hide-details
            hide-no-data
            chips
            multiple
            deletable-chips
            autofocus
            return-object
            attach="#search"
            solo
            :menu-props="{top: true, nudgeTop: 10}"
          >
            <template #append>
              <v-tooltip top z-index="10">
                <template v-slot:activator="{ on }">
                  <v-btn
                    x-small
                    fab
                    :color="(view === 1) ? 'none' : colors.Allow"
                    @click="view = (view + 1 ) % 2"
                    v-on="on"
                  >
                    <img width="25" :src="(view == 1) ? icons.AWS.Resource :  icons.AWS.Action" />
                  </v-btn>
                </template>
                <span style="z-index: 1" v-if="view === 0">
                  Switch to
                  <b>Actions</b>
                </span>
                <span style="z-index: 1" v-else-if="view === 1">
                  Switch to
                  <b>Resources</b>
                </span>
              </v-tooltip>
            </template>

            <template #selection="data">
              <v-chip v-on="data.on" close @click="data.select" @click:close="remove(data.item)">
                <v-avatar left :color="(view === 1) ? colors[data.item.access] : 'white'">
                  <img
                    :src="(view === 0) ? data.item.type.split('::').reduce((o, i) => (i in o) ? o[i] : icons.AWS.Resource, icons) : icons.AWS.Action"
                  />
                </v-avatar>
                {{ data.item.name }}
              </v-chip>
            </template>

            <template #item="data">
              <template v-on="data.on">
                <v-list-item-avatar
                  size="50"
                  style="border: 1px solid #ccc; padding: 30px;"
                  :color="(view === 1) ? colors[data.item.access] : 'none'"
                >
                  <img
                    :src="(view === 0) ? data.item.type.split('::').reduce((o, i) => (i in o) ? o[i] : icons.AWS.Resource, icons) : icons.AWS.Action"
                  />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title v-html="highlight(data.item.name)"></v-list-item-title>
                  <v-list-item-subtitle v-if="view === 0" v-html="data.item.id"></v-list-item-subtitle>
                  <v-list-item-subtitle v-else-if="view === 1" v-html="data.item.description"></v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>
        </v-card>
      </div>

      <v-card
        v-else
        :height="(hover) ? 30: 20"
        width="50"
        class="mx-auto material-icons"
        @click="show = !show"
        @mouseover="hover = true"
        @mouseleave="hover = false"
      >expand_less</v-card>
    </v-expand-transition>
  </div>
</template>

<script>
import icons from "@/icons.js";
import { access } from "@/config.js";

export default {
  name: "Search",
  props: {
    hide: {
      type: Boolean,
      default: false
    },
    alt: false
  },

  data: function() {
    return {
      search: "",
      hover: false,
      loading: false,
      items: [],
      view: 0,
      selected: [],
      actions: [],
      resources: [],
      icons: icons,
      colors: access
    };
  },

  watch: {
    selected(n, o) {
      if (n.length === o.length) {
        return;
      } else if (n.length > o.length) {
        this.add(n.filter(e => !o.includes(e)));
      }
    },

    alt(value) {
      this.view = value ? 1 : 0;
    }
  },

  methods: {
    update(s) {
      this.search = s === null ? "" : s;
    },

    filter(item, search, text) {
      return (
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        item.id.toLowerCase().includes(search.toLowerCase())
      );
    },

    highlight(value) {
      const re = new RegExp(this.search, "gi");
      let v = value.replace("<b>", "").replace("</b>");

      Array.from(new Set(v.match(re))).map(
        m => (v = v.replace(m, `<b>${m}</b>`))
      );

      return v;
    },

    add(elements) {
      if (this.view === 0)
        this.$emit(
          "add_element",
          elements.map(e => e.element)
        );
      else if (this.view === 1)
        this.$emit(
          "find_actions",
          elements.map(e => e.name)
        );
    },
    remove(item) {
      this.selected = this.selected.filter(s => s.id !== item.id);
    },
    load() {
      const types = ["Admin", "External", "Resource", "Generic"];
      this.loading = true;

      this.neo4j
        .run(
          "MATCH ()-[action:ACTION]->() " +
            "WITH DISTINCT action.Name AS name, " +
            "action.Description AS description, " +
            "action.Access AS access " +
            "RETURN name, description, access ORDER BY name"
        )
        .then(actions => {
          this.actions = actions.Text.map(a => {
            return {
              name: a.name,
              id: a.name,
              description: a.description,
              access: a.access
            };
          }).sort((a, b) => (a.name > b.name ? 1 : -1));
        });

      this.neo4j
        .run("MATCH (r) WHERE NOT (r:Pattern OR r:`AWS::Domain`) RETURN r")
        .then(elements => {
          this.resources = elements.Graph.map(r => {
            const id =
              typeof r.data.properties.Arn !== "undefined"
                ? r.data.properties.Arn
                : r.data.name;

            const classification = r.classes
              .filter(c => types.indexOf(c) != -1)
              .concat("")[0];

            return {
              name: r.data.name,
              id: id,
              type: r.data.name === "Effective Admin" ? "Admin" : r.data.type,
              class:
                r.data.name === "Effective Admin" ? "Admin" : classification,
              element: r
            };
          }).sort((a, b) => {
            let c = types.indexOf(a.class) - types.indexOf(b.class);
            if (c !== 0) return c;
            else return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
            return c;
          });
          this.items = this.resources;
        })
        .then(() => {
          this.loading = false;
        });
    }
  },

  computed: {
    show: {
      get: function() {
        return !this.hide;
      },
      set: function() {
        this.$emit("show");
      }
    }
  },
  mounted() {
    this.load();
  }
};
</script>

<style>
#search,
#search > .v-list {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  position: absolute;
  margin: auto;
  left: 0px;
  right: 0px;
  bottom: 0px;
  width: calc(75vw);
}
</style>


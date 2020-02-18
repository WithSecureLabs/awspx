<template>
  <div id="search">
    <!-- Search expansion -->
    <v-card
      :style="{display: !show ? '' : 'none'}"
      :height="(hover) ? 30: 20"
      width="50"
      class="mx-auto"
      @click="show = !show"
      @mouseover="hover = true"
      @mouseleave="hover = false"
    >
      <div class="d-flex justify-center align-center">
        <v-icon>mdi-chevron-up</v-icon>
      </div>
    </v-card>

    <!-- Autocomplete -->
    <v-expand-transition>
      <div v-if="!editor" :style="{display: show ? '' : 'none'}" class="mb-5">
        <v-card>
          <v-autocomplete
            :filter="filter"
            :items="(view == 0) ? resources : actions"
            :loading="loading"
            :cache-items="false"
            :aria-autocomplete="false"
            @input="search=null"
            :search-input.sync="search"
            v-model="selected"
            attach="#search"
            item-text="name"
            item-value="id"
            return-object
            hide-details
            hide-no-data
            clearable
            autofocus
            multiple
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
                    class="mt-n3 ml-n10"
                  >
                    <v-img width="25" :src="(view == 1) ? icons.AWS.Resource :  icons.AWS.Action" />
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

            <!-- Autocomplete selection -->
            <template #selection="data">
              <v-chip
                v-on="data.on"
                close
                outlined
                @click="data.select"
                @click:close="selected = selected.filter(s => s.id !== data.item.id)"
              >
                <v-avatar outlined :color="(view === 1) ? colors[data.item.access] : 'white'">
                  <v-img :src="icon(data.item)" />
                </v-avatar>
                <span class="ml-2" style="font-size: 11px">{{ data.item.name }}</span>
              </v-chip>
            </template>

            <!-- Autocomplete items -->
            <template #item="data">
              <template v-on="data.on">
                <v-list-item-avatar
                  size="50"
                  style="border: 1px solid #ccc; padding: 30px;"
                  :color="(view === 1) ? colors[data.item.access] : 'none'"
                >
                  <img height="50" width="50" :src="icon(data.item)" />
                </v-list-item-avatar>
                <v-list-item-content style="text-align: center">
                  <v-list-item-title v-html="highlight(data.item.name)"></v-list-item-title>
                  <v-list-item-subtitle v-if="view === 0" v-html="data.item.id"></v-list-item-subtitle>
                  <v-list-item-subtitle v-else-if="view === 1" v-html="data.item.description"></v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>
        </v-card>
      </div>
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
        const elements = n.filter(e => !o.includes(e));
        if (this.view === 0) this.add(elements.map(e => e.element));
        else if (this.view === 1)
          this.$emit(
            "find_actions",
            elements.map(e => e.name)
          );
      }
    },

    alt(value) {
      this.view = value ? 1 : 0;
    }
  },

  methods: {
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

    icon(item) {
      return this.view === 0
        ? item.type
            .split("::")
            .reduce(
              (o, i) => (i in o ? o[i] : this.icons.AWS.Resource),
              this.icons
            )
        : this.icons.AWS.Action;
    },

    add(elements) {
      this.$emit("add", elements);
    },

    load() {
      const types = ["Admin", "External", "Resource", "Generic"];
      this.loading = true;

      Promise.all([
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
          }),
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
      ]).finally(() => {
        this.loading = false;
      });
    }
  },

  computed: {
    show: {
      get: function() {
        return !this.hide;
      },
      set: function(value) {
        this.$emit("toggle", !value);
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
  transform: translateX(-50%);
  position: absolute;
  width: calc(75vw);
  margin: auto;
  bottom: 0px;
  left: 50%;
}
</style>

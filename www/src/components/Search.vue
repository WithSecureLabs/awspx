<template>
  <div>
    <div v-if="loading || populated" id="search">
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

      <!-- Search -->
      <v-expand-transition>
        <v-card v-if="mode === 'basic'" style="bottom: 10px; width: 70vw" v-show="show">
          <TemplateAutocomplete
            :resources="resources"
            :search="search"
            @add="graph_add"
            @clear="graph_clear"
            width="65vw"
          >
            <template #append>
              <v-btn text class="my-n2" small fab @click="mode = 'advanced'">
                <v-icon>mdi-cogs</v-icon>
              </v-btn>
            </template>
          </TemplateAutocomplete>
        </v-card>

        <SearchAdvanced
          v-else
          v-show="show"
          style="width: 70vw; bottom: 10px"
          :resources="resources"
          :actions="actions"
          @back="mode = 'basic'"
          @close="show = false"
          @add="graph_add"
          @clear="graph_clear"
        />
      </v-expand-transition>
    </div>

    <!-- Empty database helper -->
    <v-stepper v-else-if="!db_error" style="width: 50vw;" class="mx-auto" value="2">
      <v-stepper-header>
        <v-stepper-step step="1" complete>Install awspx</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="2">Populate database</v-stepper-step>
        <v-card></v-card>
        <v-divider></v-divider>
        <v-stepper-step step="3">Explore</v-stepper-step>
      </v-stepper-header>

      <v-stepper-content step="2">
        <v-card color="grey lighten-5" class="mb-5 pa-10">
          <v-card-title>You may have jumped the gun...</v-card-title>
          <v-card-subtitle class="mb-5">We couldn't find any data to work with</v-card-subtitle>
          <v-card-text>
            <div class="mb-2">
              <b>Either</b> run the ingestor to load an account of your own:
            </div>
            <v-card style="font-size: 11px; border: 1px solid whitesmoke;" class="pa-2">
              [root@localhost ~]#
              <b>awspx ingest</b>
              <br />[-] The profile 'default' was not found. Would you like to create it? (y/n) y
              <br />AWS Access Key ID [None]: ****9XY7
              <br />AWS Secret Access Key [None]: ****ks91
              <br />Default region name [None]: eu-west-1
              <br />Default output format [None]: json
              <br />
            </v-card>
            <div class="mt-10 mb-2">
              <b>OR</b> load an existing database (e.g. the provided sample):
            </div>
            <v-card style="font-size: 11px; border: 1px solid whitesmoke;" class="pa-2">
              <br />[root@localhost ~]#
              <b>awspx db --load-zip sample.zip</b>
              <br />[*] Importing records from /opt/awspx/data/sample.zip
              <br />
              <br />[root@localhost ~]#
              <b>awspx attacks</b>
              <br />[*] Searching database for attack patterns
              <br />
            </v-card>
          </v-card-text>
        </v-card>
        <v-btn color="primary" class="my-auto" :loading="loading" @click="load()">Check again</v-btn>
      </v-stepper-content>
    </v-stepper>
  </div>
</template>

<script>
import icons from "@/icons.js";
import { access } from "@/config.js";
import TemplateAutocomplete from "@/components/TemplateAutocomplete";
import SearchAdvanced from "@/components/SearchAdvanced";

export default {
  name: "Search",
  components: {
    SearchAdvanced,
    TemplateAutocomplete
  },
  props: {
    hide: {
      type: Boolean,
      default: false
    }
  },

  data: function() {
    return {
      mode: "basic",
      actions: [],
      resources: [],
      search: {
        label: "",
        input: "",
        value: []
      },
      hover: false,
      loading: true,
      db_error: false
    };
  },

  watch: {
    "search.value"(n, o) {
      if (n.length === o.length) {
        return;
      } else if (n.length > o.length)
        this.graph_add(n.filter(e => !o.includes(e)).map(e => e.element));
    }
  },

  methods: {
    graph_add(elements) {
      this.$emit("add", elements);
    },

    graph_clear() {
      this.$emit("clear");
    },

    load() {
      const types = ["Admin", "External", "Resource", "Generic"];
      this.loading = true;

      Promise.all([
        this.neo4j
          .run(
            "MATCH ()-[action:ACTION]->() " +
              "RETURN action ORDER BY action.Name"
          )
          .then(actions => {
            this.actions = actions.Text.map(result => {
              return JSON.parse(result["action"]);
            });
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
          })
      ]).finally(() => {
        this.db_error = Object.keys(this.neo4j.error).length > 0;
        this.search.label = `Search ${this.resources.length} Resources`;
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
    },
    populated: function() {
      return this.resources.length + this.actions.length > 0;
    },

    advanced_query: function() {
      const from = this.modes.advanced.search.From.value.map(v =>
        v.element.data.id.replace("n", "")
      );
      const to = this.modes.advanced.search.To.value.map(v =>
        v.element.data.id.replace("n", "")
      );
      const filters = this.modes.advanced.filters.map(f => f.text);

      const hops =
        typeof this.modes.advanced.hops === "number"
          ? this.modes.advanced.hops.toString()
          : "";
      const limit =
        typeof this.modes.advanced.limit === "number"
          ? this.modes.advanced.limit.toString()
          : "";

      const edges = this.modes.advanced.effective
        ? `TRANSITIVE|ATTACK*0..${hops}`
        : `TRANSITIVE*0..${hops}`;

      let query = [
        "MATCH",
        this.modes.advanced.actions
          ? `Path=(Source)-[:${edges}]->()-[Action:ACTION]->(Target)`
          : `Path=(Source)-[:${edges}]->(Target)`
      ];

      const where = [
        from.length > 0 ? [`ID(Source) IN [${from}]`] : [],
        to.length > 0 ? [`ID(Target) IN [${to}]]`] : [],
        filters
      ]
        .flat()
        .join(" AND ");

      if (where.length > 0) query.push("WHERE", where);

      query = query.concat("RETURN Path");

      if (limit !== "") query.push(`LIMIT ${limit}`);

      query = query.join(" ");
      return query;
    }
  },
  mounted() {
    this.load();
  }
};
</script>

<style>
#search {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transform: translateX(-50%);
  position: absolute;
  margin: auto;
  bottom: 0px;
  left: 50%;
}
</style>

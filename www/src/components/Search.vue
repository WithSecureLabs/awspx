<template>
  <div>
    <div v-if="loading || populated" id="search">
      <!-- Search expansion -->
      <v-card
        v-show="!show"
        @click="$emit('show', true)"
        @mouseleave="hover = false"
        :height="(hover) ? 30: 20"
        @mouseover="hover = true"
        class="mx-auto"
        width="50"
      >
        <div class="d-flex justify-center align-center">
          <v-icon>mdi-chevron-up</v-icon>
        </div>
      </v-card>

      <!-- Search -->
      <div style="bottom: 10px; width: 70vw" v-show="!advanced && show">
        <TemplateAutocomplete
          :append="{enabled: true, icon: 'mdi-tune', description: 'Advanced Search'}"
          :resources="!advanced ? resources : []"
          @append="$emit('advanced', true)"
          @add="$emit('add', $event)"
          @clear="$emit('clear')"
          :key="advanced ? 0: 1"
          :search="search"
          width="65vw"
        />
      </div>

      <SearchAdvanced
        ref="advanced"
        @visual_queries_active="$emit('visual_queries_active', $event)"
        :visual_queries_active="visual_queries_active"
        style="width: 70vw; bottom: 10px"
        @back="$emit('advanced', false)"
        @add="$emit('add', $event)"
        v-show="advanced && show"
        @clear="$emit('clear')"
        :resources="resources"
        :actions="actions"
      />
    </div>
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
    show: {
      type: Boolean,
      default: true
    },
    advanced: {
      type: Boolean,
      default: false
    },
    visual_queries_active: {
      type: Boolean,
      default: false
    }
  },

  data: function() {
    return {
      actions: [],
      resources: [],
      search: {
        label: "",
        input: "",
        value: []
      },
      populated: true,
      hover: false,
      loading: true
    };
  },

  methods: {
    init() {
      const types = ["Admin", "External", "Resource", "CatchAll", "Generic"];
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
        const count = this.resources.filter(r => r.class === "Resource").length;
        this.search.label = `Search ${count} Resources  (+${this.resources.length - count} others)`;
        this.loading = false;
      });
    }
  },

  watch: {
    resources() {
      this.populated = this.resources.length + this.actions.length > 0;
    },
    actions() {
      this.populated = this.resources.length + this.actions.length > 0;
    },
    populated(value) {
      this.$emit("populated", value);
    },
    "search.value"(n, o) {
      if (n.length === o.length) {
        return;
      } else if (n.length > o.length)
        this.$emit(
          "add",
          n.filter(e => !o.includes(e)).map(e => e.element)
        );
    }
  },

  computed: {
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
    this.init();
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

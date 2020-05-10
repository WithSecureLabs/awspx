<template>
  <!-- Query editor -->
  <div id="search-advanced">
    <v-card :disabled="neo4j.busy">
      <!-- Visual -->
      <v-form v-model="valid.form" ref="visual">
        <v-card-text>
          <span
            class="overline ml-5"
            color="primary"
            style="font-size: 12px !important; color: rgb(25, 118, 210);"
          >Advanced Search</span>

          <v-row
            v-show="!editor.fullscreen"
            no-gutters
            class="mx-5 pt-2 flex-nowrap"
            align="center"
          >
            <!-- 'To' and 'From' -->
            <v-col class="text-left">
              <TemplateAutocomplete
                :resources="resources"
                :actions="actions"
                :search="visual.search.From"
                :disabled="!visual.enabled"
                :placeholder="true"
                width="50vw"
              />
              <!-- Swap 'From' and 'To' around -->
              <div class="ma-n5 px-5 text-center">
                <v-btn :disabled="!visual.enabled" @click="visual_swap" x-small icon fab>
                  <v-icon size="16">mdi-cached</v-icon>
                </v-btn>
              </div>
              <TemplateAutocomplete
                :resources="resources"
                :actions="actions"
                :search="visual.search.To"
                :disabled="!visual.enabled"
                :placeholder="true"
                width="50vw"
              />
            </v-col>

            <!-- Advanced options -->
            <v-col justify="center" class="pl-10 mt-n3" cols="2">
              <v-card flat :disabled="!visual.enabled" width="170px">
                <fieldset class="search-mode">
                  <legend class="mx-2 my-n3">
                    <span class="px-1">Mode</span>
                  </legend>
                  <v-row class="text-center">
                    <v-switch v-model="visual.actions" class="mx-auto">
                      <template #prepend>
                        <v-tooltip left>
                          <template v-slot:activator="{ on }">
                            <v-icon
                              v-on="on"
                              :color="visual.actions ? '' : 'primary'"
                              @click="visual.actions = false"
                            >mdi-map-marker-outline</v-icon>
                          </template>
                          <span width="300px">
                            <b>Paths-based search</b>
                            <br />See what can get to what
                          </span>
                        </v-tooltip>
                      </template>

                      <template #append>
                        <v-tooltip right>
                          <template v-slot:activator="{ on }">
                            <v-icon
                              v-on="on"
                              :value="true"
                              :color="visual.actions ? 'primary' : ''"
                              @click="visual.actions = true"
                            >mdi-chevron-right-circle-outline</v-icon>
                          </template>

                          <span width="300px">
                            <b>Actions-based search</b>
                            <br />See what can do what to what
                          </span>
                        </v-tooltip>
                      </template>
                    </v-switch>
                  </v-row>

                  <v-row class="text-center">
                    <v-switch v-model="visual.effective" false-value class="mx-auto">
                      <template #prepend>
                        <v-tooltip left>
                          <template v-slot:activator="{ on }">
                            <v-icon
                              v-on="on"
                              :color="visual.effective ? '' : 'primary'"
                              @click="visual.effective = false"
                            >mdi-arrow-top-right</v-icon>
                          </template>
                          <span width="300px">
                            <b>Direct search</b>
                            <br />Exclude attack paths
                          </span>
                        </v-tooltip>
                      </template>

                      <template #append>
                        <v-tooltip right>
                          <template v-slot:activator="{ on }">
                            <v-icon
                              v-on="on"
                              :color="visual.effective ? 'primary' : ''"
                              @click.stop="visual.effective = true"
                              value="false"
                            >mdi-map-marker-path</v-icon>
                          </template>
                          <span width="300px">
                            <b>Effective search</b>
                            <br />Include attack paths
                          </span>
                        </v-tooltip>
                      </template>
                    </v-switch>
                  </v-row>
                </fieldset>
              </v-card>
            </v-col>
          </v-row>

          <!-- Add filters or limit results -->
          <v-row no-gutters align="center" class="mb-n5">
            <v-col v-show="!editor.fullscreen">
              <div style="width: 450px">
                <v-row class="mx-5 mt-5" no-gutters>
                  <v-col>
                    <v-btn
                      :disabled="!visual.enabled"
                      outlined
                      small
                      color="primary"
                      @click="visual_filter_add()"
                    >Add filter</v-btn>
                  </v-col>

                  <v-col>
                    <v-text-field
                      :rules="[(v) => (v == '' || !isNaN(v)) || 'invalid integer value']"
                      class="limit pa-0 ma-0 mr-5 ml-n1 overline"
                      :aria-autocomplete="false"
                      :disabled="!visual.enabled"
                      placeholder="UNLIMITED"
                      v-model="visual.limit"
                      label="#Results"
                      color="primary"
                      outlined
                    >
                      <template #append>
                        <v-icon
                          v-if="visual.limit !== ''"
                          class="mt-n3"
                          small
                          @click="visual.limit = ''"
                        >mdi-close</v-icon>
                      </template>
                    </v-text-field>
                  </v-col>

                  <v-col>
                    <v-text-field
                      :rules="[(v) => (v == '' || !isNaN(v)) || 'invalid integer value']"
                      class="limit pa-0 ma-0 overline"
                      :disabled="!visual.enabled"
                      :aria-autocomplete="false"
                      placeholder="UNLIMITED"
                      v-model="visual.hops"
                      color="primary"
                      label="#Hops"
                      outlined
                    >
                      <template #append>
                        <v-icon
                          v-if="visual.hops !== ''"
                          class="mt-n3"
                          small
                          @click="visual.hops = ''"
                        >mdi-close</v-icon>
                      </template>
                    </v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-col>

            <!-- Load saved query -->
            <v-col>
              <v-autocomplete
                ref="saved_queries"
                class="mx-5 saved-queries overline primary--text"
                @blur="$emit('visual_queries_active', false)"
                @focus="$emit('visual_queries_active', true)"
                :class="editor.fullscreen ? 'mt-n8' : ''"
                :menu-props="{top: true, nudgeTop: 10}"
                style="width: 30vw; float: right"
                placeholder="LOAD A SAVED QUERY"
                v-model="visual.queries.loaded"
                :items="visual.queries.saved"
                item-value="description"
                item-text="name"
                return-object
                clearable
              >
                <template #prepend-inner>
                  <v-icon
                    :color="visual.queries.loaded  ? 'primary' : ''"
                    class="mx-5 pa-0"
                  >mdi-content-save-edit</v-icon>
                </template>

                <template #item="data">
                  <v-tooltip right>
                    <template v-slot:activator="{ on }">
                      <v-icon x-small v-on="on" class="mr-5">mdi-help-circle-outline</v-icon>
                      <div class="overline" flat>{{data.item.name}}</div>
                    </template>
                    <span>{{data.item.description}}</span>
                  </v-tooltip>
                </template>

                <template #selection="data">
                  <div class="overline">{{data.item.name}}</div>
                </template>
              </v-autocomplete>
            </v-col>
          </v-row>

          <!-- Filters -->
          <div
            v-show="visual.filters.length > 0 && !editor.fullscreen"
            style="max-height: 25vh; overflow-y: auto;"
            class="pb-1"
          >
            <v-expansion-panels
              :class="!visual.enabled ? 'readonly' : ''"
              :value="visual.enabled"
              class="px-5"
              accordion
            >
              <v-expansion-panel
                v-for="(_, j) in visual.filters"
                :disabled="!visual.enabled"
                :key="'filter-' + j"
              >
                <v-expansion-panel-header class="pa-3 my-n3">
                  <template #default>
                    <v-col>
                      <v-row
                        style="color: rgba(0,0,0,0.4) !important; font-size: 13px"
                        align="center"
                      >
                        <div v-if="visual.filters[j].valid">
                          <v-icon class="mr-5" color="primary">mdi-filter</v-icon>
                          <span style="color: rgba(0,0,0,0.7); font-size: 13px">
                            {{(j === 0 ? "": visual.filters[j].and ? "AND " : "OR ") +
                            visual.filters[j].text}}
                          </span>
                        </div>
                        <div v-else>
                          <v-icon class="mr-5" color="primary">mdi-filter-outline</v-icon>
                          <span>Unconfigured</span>
                        </div>
                      </v-row>
                    </v-col>
                    <v-btn
                      v-if="j !== 0"
                      @click.stop="visual.filters[j].and = !visual.filters[j].and"
                      background-color="primary"
                      icon
                    >
                      <span v-if="visual.filters[j].and">⋂</span>
                      <span v-if="!visual.filters[j].and">⋃</span>
                    </v-btn>
                    <v-btn icon @click.stop="visual_filter_remove(j)">
                      <v-icon color="error">mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <SearchAdvancedFilter
                    :options="{actions: visual.actions, effective: visual.effective}"
                    :sources="visual.search.From.value"
                    :targets="visual.search.To.value"
                    :resources="resources"
                    :actions="actions"
                    :filter="visual.filters[j]"
                    @filter_update="visual_filter_update(j, $event)"
                  ></SearchAdvancedFilter>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-card-text>
      </v-form>

      <!-- Editor (adapted from https://github.com/neo4j-contrib/cypher-editor) -->
      <div class="mt-n3 px-5">
        <div style="width: 100%" class="text-right ml-n2 mb-n8">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                @click.stop="editor.fullscreen = !editor.fullscreen"
                style="z-index: 3; background-color: white;"
                color="rgba(25, 118, 210, 0.7)"
                x-small
                icon
              >
                <v-icon>{{ editor.fullscreen ? 'mdi-window-restore': 'mdi-arrow-expand'}}</v-icon>
              </v-btn>
            </template>
            <span>{{editor.fullscreen ? 'Restore' : 'Expand Editor' }}</span>
          </v-tooltip>
        </div>
        <v-card-text
          id="editor"
          :class="[!editor.settings.readOnly ? '' : 'readonly', editor.fullscreen ? 'fullscreen' : '']"
          @input="editor.settings.value = editor.value.getValue()"
        />
        <div style="width: 100%;" class="text-center mt-n8">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                style="z-index: 3; background-color: white;"
                @click.stop="editor_readonly_toggle"
                :disabled="!editor.button"
                color="rgba(25, 118, 210, 0.7)"
                depressed
                outlined
                x-small
                fab
              >
                <v-icon>{{ editor.settings.readOnly ? 'mdi-lock-outline' : 'mdi-lock-open-variant-outline' }}</v-icon>
              </v-btn>
            </template>
            <span>{{ editor.settings.readOnly ? 'Enable Editor' : 'Disable Editor' }}</span>
          </v-tooltip>
        </div>
      </div>

      <!-- Buttons -->
      <v-row class="mx-5 flex-nowrap">
        <v-col cols="1">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" outlined color="primary" @click="$emit('back')">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
            </template>
            <b>Back</b>
          </v-tooltip>
        </v-col>

        <v-col cols="1">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                outlined
                color="primary"
                :disabled="visual.results.items.length === 0"
                @click="visual.results.enabled = true"
              >
                <v-badge
                  :value="visual.results.items.length > 0"
                  :content="visual.results.items.length"
                >
                  <v-icon>mdi-file-table</v-icon>
                </v-badge>
              </v-btn>
            </template>
            <span>
              View
              <b>Textual Results</b>
            </span>
          </v-tooltip>
        </v-col>

        <v-col cols="9" />
        <v-col cols="1" class="text-center">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                outlined
                color="primary"
                :disabled="!visual_valid"
                @click="editor_run"
              >
                <v-icon>mdi-play</v-icon>
              </v-btn>
            </template>
            <span>
              <b>Run</b>
            </span>
          </v-tooltip>
        </v-col>
      </v-row>
    </v-card>

    <!-- Textual results -->
    <SearchResultsTable
      :data="visual.results.items"
      :enabled="visual.results.enabled"
      @close="visual.results.enabled = false"
    />
  </div>
</template>

<script>
import * as CypherCodeMirror from "@/codemirror-cypher/cypher-codemirror.min.js";
import codemirror from "codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/addon/lint/lint";
import "codemirror/addon/lint/lint.css";
import "codemirror/addon/hint/show-hint";
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/display/autorefresh";

import { queries } from "@/queries.js";

import SearchAdvancedFilter from "@/components/SearchAdvancedFilter";
import TemplateAutocomplete from "@/components/TemplateAutocomplete";
import TemplateSelectSearch from "@/components/TemplateSelectSearch";
import TemplateSelectItem from "@/components/TemplateSelectItem";
import SearchResultsTable from "@/components/SearchResultsTable";

export default {
  name: "SearchAdvanced",
  components: {
    SearchAdvancedFilter,
    SearchResultsTable,
    TemplateAutocomplete,
    TemplateSelectSearch,
    TemplateSelectItem
  },
  props: {
    resources: {
      Type: Array,
      default: []
    },
    actions: {
      Type: Array,
      default: []
    },
    visual_queries_active: {
      Type: Boolean,
      default: false
    }
  },

  data: function() {
    return {
      visual: {
        enabled: true,
        search: {
          From: { input: "", value: [], label: "From" },
          To: { input: "", value: [], label: "To" }
        },
        queries: {
          loaded: undefined,
          saved: queries,
          active: false
        },
        results: {
          items: [],
          enabled: false,
          active: false
        },
        effective: true,
        actions: false,
        reverse: false,
        filters: [],
        limit: 500,
        hops: ""
      },
      editor: {
        enabled: true,
        value: {},
        fullscreen: false,
        button: true,
        settings: {
          value: "",
          autoRefresh: true,
          mode: "application/x-cypher-query",
          readOnly: "nocursor",
          indentWithTabs: false,
          smartIndent: false,
          lineNumbers: true,
          matchBrackets: true,
          autofocus: true,
          lint: true,
          styleActiveLine: true,
          extraKeys: {
            Tab: "autocomplete",
            "Ctrl-R": this.editor_run
          },
          hintOptions: {
            completeSingle: false,
            closeOnUnfocus: false,
            alignWithWord: true,
            async: true
          },
          gutters: ["cypher-hints"],
          lineWrapping: true,
          autoCloseBrackets: {
            explode: ""
          },

          neo4jSchema: {
            consoleCommands: [],
            labels: [],
            relationshipTypes: [],
            parameters: [],
            propertyKeys: [],
            functions: [],
            procedures: []
          }
        }
      },
      loading: false,
      valid: {
        form: true,
        filters: true
      }
    };
  },

  methods: {
    editor_run() {
      this.loading = true;
      this.visual.results.enabled = false;
      this.visual.results.items = [];
      this.$emit("clear");
      this.editor.settings.value = this.editor.value.getValue();

      if (this.editor.settings.value === "") return;

      this.neo4j
        .run(this.editor.settings.value)
        .then(results => {
          this.visual.results.items = results.Text;
          if (results.Graph.length > 0) this.$emit("add", results.Graph);
          else if (results.Text.length > 0) this.visual.results.enabled = true;
        })
        .finally(() => {
          this.loading = false;
        });
    },

    editor_autocomplete(cm, changed) {
      if (changed.text.length !== 1) {
        return;
      }
      const text = changed.text[0];
      const shouldautocomplete =
        text === "." ||
        text === ":" ||
        text === "[]" ||
        text === "()" ||
        text === "{}" ||
        text === "[" ||
        text === "(" ||
        text === "{" ||
        text === "$";
      if (shouldautocomplete) {
        cm.execCommand("autocomplete");
      }
    },

    editor_readonly_toggle() {
      this.editor.settings.readOnly =
        this.editor.settings.readOnly === "nocursor" ? false : "nocursor";
    },

    visual_swap() {
      const from = this.visual.search.From.value;
      const to = this.visual.search.To.value;

      this.visual.search.To.value = from;
      this.visual.search.From.value = to;
      this.visual.reverse = !this.visual.reverse;
    },

    visual_filter_add() {
      this.visual.filters.push({ valid: false, text: "", and: true });
    },

    visual_filter_update(i, e) {
      Object.keys(e).forEach(k => {
        this.visual.filters[i][k] = e[k];
      });
    },

    visual_filter_remove(i) {
      const removed = this.visual.filters.splice(i, 1);
      if (this.visual.filter === i) this.visual.filter = -1;
    },

    visual_query_load(cypher) {
      const lines = cypher.split("\n");
      this.editor.value.setValue(cypher);
      this.editor.value.setCursor({
        line: lines.length,
        ch: lines.splice(-1).length
      });
    }
  },

  watch: {
    visual_queries_active(value) {
      if (value) {
        this.$refs.saved_queries.focus();
        this.$refs.saved_queries.activateMenu();
        this.$emit("visual_queries_active", false);
      }
    },

    visual_query(query) {
      this.$refs.visual.validate();
      this.visual_query_load(query);
    },

    "editor.settings.readOnly"(value) {
      this.editor.value.setOption("readOnly", value);
      this.visual.enabled = !!value;
    },

    "visual.queries.loaded"(load) {
      if (typeof load === "undefined") {
        this.editor.button = true;
        this.editor.settings.readOnly = "nocursor";
        this.visual_query_load(this.visual_query);
      } else {
        this.editor.button = false;
        this.editor.settings.readOnly = false;
        this.visual_query_load(
          `/* ${load.description} */\n${load.value.join("\n")}`
        );
      }
    },

    "visual.filters": {
      handler: function() {
        this.valid.filters = this.visual.filters.every(f => f.valid);
      },
      deep: true
    }
  },

  computed: {
    visual_valid() {
      return this.valid.form && this.valid.filters;
    },

    visual_query() {
      const from = this.visual.search.From.value.map(v =>
        v.element.data.id.replace("n", "")
      );
      const to = this.visual.search.To.value.map(v =>
        v.element.data.id.replace("n", "")
      );
      const filters = this.visual.filters
        .filter(f => f.valid)
        .map((f, i) => {
          return i === 0 ? f.text : (f.and ? "AND " : "OR ") + f.text;
        })
        .join("\n");

      const hops =
        this.visual.hops === null || isNaN(this.visual.hops)
          ? ""
          : this.visual.hops;
      const limit =
        this.visual.limit === null || isNaN(this.visual.limit)
          ? ""
          : this.visual.limit;

      const edges = this.visual.effective
        ? `TRANSITIVE|ATTACK*0..${hops}`
        : `TRANSITIVE*0..${hops}`;

      let query = [
        "MATCH",
        this.visual.actions
          ? `Paths=ShortestPath((Source)-[:${edges}]->(Entity)),` +
            `\n      Actions=(Entity)-[Action:ACTION]->(Target)`
          : `Paths=ShortestPath((Source)-[:${edges}]->(Target))`
      ];

      const where = [
        from.length > 0 ? `ID(Source) IN [${from}]` : undefined,
        to.length > 0 ? `ID(Target) IN [${to}]` : undefined,
        filters.length > 0 ? `(${filters})` : undefined
      ]
        .filter(f => typeof f === "string")
        .join("\nAND ");

      if (where.length > 0) query.push("\nWHERE", where);

      query.push(`\nRETURN Paths${this.visual.actions ? ", Actions" : ""}`);

      if (limit !== "") query.push(`LIMIT ${limit}`);

      return query.join(" ");
    }
  },

  mounted() {
    Promise.all(
      // Populate visual query editor settings
      [
        this.neo4j.run("CALL db.labels()").then(r => {
          this.editor.settings.neo4jSchema.labels = r.Text.map(
            l => `:${l["label"]}`
          )
            .filter(
              l =>
                l.includes("::") ||
                [":Admin", ":Resource", ":Generic", ":External"].includes(l)
            )
            .sort();
        }),
        this.neo4j.run("CALL db.relationshipTypes()").then(r => {
          this.editor.settings.neo4jSchema.relationshipTypes = r.Text.map(
            rt => `:${rt["relationshipType"]}`
          );
        }),
        this.neo4j.run("CALL db.propertyKeys()").then(r => {
          this.editor.settings.neo4jSchema.propertyKeys = r.Text.map(
            p => p["propertyKey"]
          );
        }),

        this.neo4j.run("CALL dbms.functions()").then(r => {
          this.editor.settings.neo4jSchema.functions = r.Text;
        }),

        this.neo4j.run("CALL dbms.procedures()").then(r => {
          this.editor.settings.neo4jSchema.procedures = r.Text;
        })
      ]
    ).then(() => {
      const { editor, editorSupport } = CypherCodeMirror.createCypherEditor(
        document.getElementById("editor"),
        this.editor.settings
      );
      editorSupport.setSchema(this.editor.settings.neo4jSchema);
      editor.setOption("theme", "cypher");
      editor.on("change", this.editor_autocomplete);

      this.editor.value = editor;
      this.visual_query_load(this.visual_query);
    });
  }
};
</script>

<style>
@import "../codemirror-cypher/cypher-codemirror.css";

.search-mode {
  border: 0.5px solid rgba(0, 0, 0, 0.3);
  color: rgba(0, 0, 0, 0.5);
  border-radius: 4px 4px;
}

.CodeMirror {
  max-height: 15vh;
  border: 1px solid rgba(25, 118, 210, 0.3);
  border-radius: 4px 4px;
}

.CodeMirror-vscrollbar {
  right: 2px;
  top: 12px;
}

.fullscreen .CodeMirror {
  height: 15vh !important;
}

.readonly .CodeMirror {
  border: 1px solid rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.readonly .v-expansion-panel-header,
.readonly .v-expansion-panel-content,
.readonly .CodeMirror-scroll,
.readonly .CodeMirror-sizer,
.readonly .CodeMirror-gutter,
.readonly .CodeMirror-gutters,
.readonly .CodeMirror-linenumber {
  opacity: 0.7;
}

.limit .v-input__slot {
  min-height: 0px !important;
  height: 28px !important;
  width: 120px;
}

.saved-queries input::placeholder {
  font-family: "Roboto Mono", monospace;
  font-size: 12px;
}

.search-advanced .mdi-close {
  font-size: 14px !important;
}
</style>
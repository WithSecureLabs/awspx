<template>
  <div class="properties" v-if="properties">
    <template>
      <!-- Tab titles -->
      <v-tabs v-model="tab" class="elevation-24" color="black" grow>
        <v-tab
          style="font-size: 12px !important"
          v-for="(tab, i) in tabs"
          :key="'title-' + i"
          :disabled="(tabs[i].content.length == 0)"
          class="text-none"
        >{{tabs[i].title}}</v-tab>
        <v-tab v-if="notes.enabled" style="font-size: 12px !important" class="text-none">Notes</v-tab>
      </v-tabs>

      <!-- Tab content -->
      <v-tabs-items v-model="tab">
        <v-tab-item v-for="(tab, i) in tabs" :key="'content' + i">
          <v-data-iterator
            :items="tabs[i].content"
            :items-per-page="10"
            :hide-default-footer="(tabs[i].content.length <= 10)"
          >
            <template v-slot:default="props">
              <v-card :raised="true" :outlined="true">
                <v-card v-for="(item, i) in props.items" :key="'item-' + i" flat tile>
                  <v-row no-gutters class="mx-0">
                    <v-col>
                      <!-- Action -->
                      <v-row
                        class="mx-2 my-0"
                        v-if="tab.style === 'action' && item.key !== 'Condition'"
                      >
                        <v-col cols="4">
                          <a v-if="'href' in item" :href="item.href" target="_blank">{{item.key}}</a>
                          <div v-else>{{item.key}}</div>
                        </v-col>
                        <v-col cols="8" class="grey--text">
                          <div v-if="Array.isArray(item.value)">
                            <div v-if="item.value.length > 0">
                              <li v-for="k in item.value" :key="'li-' + k">{{k}}</li>
                            </div>
                            <div v-else>-</div>
                            <div class="pt-1" v-if="(item.key === 'Condition Keys')">
                              +
                              <a
                                href="https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html"
                                target="_blank"
                              >
                                <i>Global Conditions</i>
                              </a>
                            </div>
                          </div>
                          <div v-else>{{item.value}}</div>
                        </v-col>
                      </v-row>

                      <!-- Codeblock (i.e. policy or action condition) -->
                      <v-card
                        flat
                        class="pt-5 ma-2"
                        v-else-if="tab.style === 'codeblock' || tab.style == 'action'"
                      >
                        <v-row class="ma-5 codeblock" v-html="item.value"></v-row>
                        <v-row>
                          <v-col
                            align="right"
                            class="mx-5 mt-n3 overline"
                            style="font-size: 9px !important"
                          >{{item.key}}</v-col>
                        </v-row>
                      </v-card>

                      <!-- Actions -->
                      <v-expansion-panels v-else-if="tab.style === 'actions'" :accordian="true">
                        <v-expansion-panel>
                          <v-expansion-panel-header>
                            {{item.name}}
                            <template v-slot:actions>
                              <v-tooltip left>
                                <template v-slot:activator="{ on }">
                                  <v-icon
                                    v-on="on"
                                    :color="(item.effect.includes('Allow')) ? 'green' : 'red'"
                                    :class="(item.effect.includes('Conditional')) ? 'conditional-action' : ''"
                                  >mdi-chevron-down</v-icon>
                                </template>
                                <span>{{item.effect}}</span>
                              </v-tooltip>
                            </template>
                          </v-expansion-panel-header>
                          <v-expansion-panel-content
                            class="font-weight-thin ma-5px"
                          >{{item.description}}</v-expansion-panel-content>
                        </v-expansion-panel>
                      </v-expansion-panels>

                      <!-- Attacks -->
                      <v-card class="pt-5 ma-2" flat v-else-if="tab.style === 'attack'">
                        <v-row class="ma-2" no-gutters>
                          <v-col cols="12">
                            <div style="width: 60px; float: left">Step {{i + 1}}:</div>
                            <div
                              style="width: calc(100% - 70px); float: left;"
                              class="grey--text"
                            >{{item.description}}</div>
                          </v-col>
                          <v-row class="mx-0" align="center">
                            <v-col>
                              <v-card>
                                <div class="codeblock" v-html="item.command"></div>
                              </v-card>
                            </v-col>
                          </v-row>
                        </v-row>
                      </v-card>

                      <!-- Standard case properties comprise of key, value pairs -->
                      <v-row class="mx-0" v-else>
                        <v-col cols="5">{{item.key}}</v-col>
                        <v-col cols="7" class="grey--text">{{item.value}}</v-col>
                      </v-row>
                    </v-col>
                  </v-row>
                </v-card>
              </v-card>
            </template>
          </v-data-iterator>
        </v-tab-item>

        <!-- Notes -->
        <v-tab-item v-if="notes.enabled">
          <v-row>
            <v-col align="center">
              <v-card :raised="true" :outlined="true">
                <v-textarea
                  outlined
                  auto-grow
                  full-width
                  clearable
                  :value="notes.value"
                  @input="notes_save"
                  class="mx-8 mt-8"
                  :rules="[notes.connected || 'Database disconnected, changes will not be saved']"
                ></v-textarea>
              </v-card>
            </v-col>
          </v-row>
        </v-tab-item>
      </v-tabs-items>
    </template>
  </div>
</template>

<script>
import icons from "@/icons.js";
import config from "@/config.js";
import cytoscape from "cytoscape";

export default {
  name: "Properties",
  props: {
    properties: {}
  },
  data: function() {
    return {
      tab: null,
      tabs: {},
      icons: icons,
      element: {},
      notes: {
        value: "",
        enabled: false,
        connected: false
      }
    };
  },
  watch: {
    properties: function(element) {
      if (element) {
        this.element = element;
        this.view_set(element);
      } else {
        this.unset();
      }
    }
  },

  methods: {
    notes_save(value) {
      const id = this.element.data.id;
      this.notes.value = value;
      this.neo4j
        .run(
          (id.charAt(0) === "n"
            ? `MATCH (e) WHERE ID(e) = ${id.substring(1)}`
            : `MATCH ()-[e]->() WHERE ID(e) = ${id.substring(1)}`) +
            ` SET e.Notes = "${this.notes.value}"`,
          false
        )
        .then(() => {
          this.notes.connected = true;
        })
        .catch(e => {
          this.notes.connected = false;
        });
    },

    notes_load() {
      const id = this.element.data.id;
      let value = "";
      this.neo4j
        .run(
          (id.charAt(0) === "n"
            ? `MATCH (e) WHERE ID(e) = ${id.substring(1)}`
            : `MATCH ()-[e]->() WHERE ID(e) = ${id.substring(1)}`) +
            ` RETURN e.Notes AS Notes`,
          false
        )
        .then(n => {
          value = n.Text[0]["Notes"] == null ? "" : n.Text[0]["Notes"];
          this.notes.connected = true;
        })
        .catch(e => {
          this.notes.connected = false;
        })
        .finally(() => {
          this.notes.value = value;
        });
    },

    view_set(element) {
      let tabs = [];
      this.notes.enabled = true;

      if (
        element.classes.includes("ACTIONS") &&
        element.data.properties != null
      ) {
        tabs.push.apply(tabs, this.view_set_actions(element));
      } else if (element.classes.includes("ACTION")) {
        tabs.push(this.view_set_action(element));
      } else if (element.classes.includes("ATTACK")) {
        tabs.push(this.view_set_attack(element));
      } else {
        tabs.push.apply(tabs, this.view_set_default(this.element));
      }

      this.tab = null;
      this.tabs = tabs;

      if (this.notes.enabled) this.notes_load();
    },

    view_set_default(element) {
      let tabs = [];
      let properties = {};
      let property_tabs = [];

      // Name is mandatory
      properties["Name"] = element.data.properties["Name"];

      // Arn is common (present in all resources and generics)
      if ("Arn" in element.data.properties)
        properties["Arn"] = element.data.properties["Arn"];

      // Sort keys where Name and Arn are always first (Notes are ignored and placed last)
      Object.keys(element.data.properties)
        .sort()
        .forEach(key => {
          let value = element.data.properties[key];
          if (
            // These keys are handled specially
            key !== "Name" &&
            key !== "Arn" &&
            key !== "Notes" &&
            // Do not present tabs with empty JSON data
            value !== "{}" &&
            value !== "[]"
          ) {
            // Skip JSON values (processed later as additional tabs)
            if (value[0] === "{" || value[0] === "[") {
              property_tabs[key] = element.data.properties[key];
            } else properties[key] = element.data.properties[key];
          }
        });

      // Properties tab (Primary)

      properties = Object.keys(properties).map(k => {
        return { key: k, value: properties[k] };
      });

      tabs.push({
        title: "type" in element.data ? element.data.type : "Properties",
        content: properties,
        style: "properties"
      });

      // Handle JSON values (Secondary)
      for (let key in property_tabs) {
        let title = key;
        let content = JSON.parse(property_tabs[key]);

        // Documents
        if (title.includes("Document") && Array.isArray(content)) {
          for (let i in content) {
            content[i] = Object.keys(content[i]).map(k => {
              return {
                key: k,
                value: JSON.stringify(content[i][k], null, 2)
                  .replace(/ /g, "&nbsp;")
                  .replace(/\n/g, "<br>")
              };
            });
          }
          content = [].concat.apply([], content);

          //Everything else
        } else
          content = [
            {
              key: "",
              value: JSON.stringify(content, null, 2)
                .replace(/ /g, "&nbsp;")
                .replace(/\n/g, "<br>")
            }
          ];

        tabs.push({
          title: title,
          content: content,
          style: "codeblock"
        });
      }
      return tabs;
    },

    view_set_actions(element) {
      let tabs = [];

      Object.keys(element.data.properties).map(k => {
        let actions = {};

        element.data.properties[k].map(e => {
          const name = e.data.name;
          let effect = e.data.properties.Effect;
          effect = (e.classes.includes("Conditional")
            ? `Conditional ${effect}`
            : effect
          ).toString();

          if (name in actions) {
            const precedence = [
              "Deny",
              "Conditional Allow",
              "Conditional Deny",
              "Allow",
              "Soft Deny" //Default, this should never be matched
            ];

            if (
              precedence.indexOf(effect) <
              precedence.indexOf(actions[name].effect)
            ) {
              actions[name].effect = effect;
            }
          } else
            actions[name] = {
              description: e.data.properties.Description,
              access: e.data.properties.Access,
              effect: effect
            };
        });
        actions = Object.keys(actions)
          .sort()
          .map(k => {
            return { name: k, ...actions[k] };
          });

        tabs.push({
          title: k,
          content: actions,
          style: "actions"
        });
      });

      this.notes.enabled = false;
      return tabs;
    },

    view_set_action(element) {
      const hrefs = {
        // "Condition Keys":
        //   "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html#context_keys_table",
        // Global:
        //   "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html"
      };
      let properties = Object.keys(element.data.properties)
        .sort()
        .filter(
          k =>
            ![
              "Name",
              "Description",
              "Condition",
              "Reference",
              "Condition Keys",
              "Dependant Actions"
            ].includes(k) && element.data.properties[k].length > 0
        )
        .map(k => {
          let item = { key: k, value: element.data.properties[k] };
          // if (
          //   k === "Description" &&
          //   "Reference" in element.data.properties &&
          //   element.data.properties["Reference"] !== ""
          // )
          //   item["href"] = element.data.properties["Reference"];
          return item;
        });

      ["Condition Keys", "Dependant Actions"].forEach(property => {
        if (property in element.data.properties) {
          properties.push({
            key: property,
            value: JSON.parse(element.data.properties[property]).sort()
          });
          if (property in hrefs) properties.slice(-1)[0].href = hrefs[property];
        }
      });

      if ("Condition" in element.data.properties) {
        properties.push({
          key: "Condition",
          value: JSON.stringify(
            JSON.parse(element.data.properties["Condition"]),
            null,
            2
          )
            .replace(/ /g, "&nbsp;")
            .replace(/\n/g, "<br>")
        });
      }

      properties.unshift({
        key: "Description",
        value: element.data.properties["Description"]
      });

      properties.push({
        key: "API Reference",
        href: element.data.properties["Reference"],
        value: ""
      });

      return {
        title: element.data.properties.Name,
        content: properties,
        style: "action"
      };
    },

    view_set_attack(element) {
      let attacks = [];
      let descriptions = element.data.properties.Descriptions || [];
      let commands = element.data.properties.Commands || [];

      commands.forEach(function(part, i) {
        this[i] = String(this[i])
          .replace(/ --/g, "&nbsp;\\<br>" + "&nbsp;".repeat(2) + "--")
          .replace(/<<EOF/g, "&lt;&lt;EOF")
          .replace(/ /g, "&nbsp;")
          .replace(/\n/g, "<br>");
      }, commands);

      let j = 0;
      for (let i = 0; i < commands.length; i++) {
        if (i > 0 && descriptions[i - 1] == descriptions[i]) {
          attacks[j - 1].command += "<br><br>" + commands[i];
        } else {
          attacks[j] = { command: commands[i], description: descriptions[i] };
          j++;
        }
      }

      return {
        title: "Attack Path",
        content: attacks,
        style: "attack"
      };
    },

    unset() {
      this.tabs = [];
    }
  }
};
</script>

<style scoped>
.properties {
  margin-top: 10px;
  margin-left: 10px;
  text-align: left;
  max-width: 40%;
}

.list-item {
  padding: 5px;
}

.list-item-inner {
  align-content: stretch;
}

.codeblock-name {
  color: gray;
  text-align: right;
  margin-right: 15px;
  font-size: x-small;
}
.codeblock {
  background: #292929;
  color: #fafafa;
  font-size: 12px;
  border: 15px solid #292929;
  border-radius: 5px;
}

.notes {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 600px;
  height: 600px;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: 1px solid black;
}

.save-notes {
  background-color: black;
  border: none;
  color: white;
  padding: 5px 15px;
  text-align: center;
  text-decoration: none;
  float: right;
}

.conditional-action {
  -webkit-text-fill-color: white;
  -webkit-text-stroke-width: 1px;
}
</style>

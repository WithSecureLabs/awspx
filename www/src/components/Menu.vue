<template>
  <div id="menu">
    <v-navigation-drawer absolute permanent right width="60">
      <template v-slot:prepend>
        <v-list dense>
          <!-- Configure Layout -->
          <v-list-item class="pa-0">
            <v-menu v-model="layout.enabled" offset-x left>
              <template v-slot:activator="{ on: menu }">
                <v-tooltip left :disabled="layout.enabled">
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn v-on="{ ...tooltip, ...menu }" depressed block color="white">
                      <template #default>
                        <v-icon>mdi-view-dashboard-outline</v-icon>
                      </template>
                    </v-btn>
                  </template>
                  <span>Configure Layout</span>
                </v-tooltip>
              </template>
              <v-list dense class="text-center primary--text">
                <v-list-item-group mandatory v-model="layout.value">
                  <v-list-item v-for="(item, i) in layout.values" :key="'menu-item-' + i">
                    <v-list-item-title>{{ item }}</v-list-item-title>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-menu>
          </v-list-item>

          <!-- Database -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    color="white"
                    class="pa-0"
                    v-on="on"
                    depressed
                    block
                    @click="$emit('database', true)"
                  >
                    <template #default>
                      <v-icon>mdi-database-edit</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>Configure database</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>

          <!-- Clear -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    depressed
                    block
                    color="white"
                    class="pa-0"
                    width="100%"
                    @click="$emit('clear')"
                  >
                    <template #default>
                      <v-icon>mdi-monitor-clean</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>Clear the screen</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>

          <!-- Screenshot -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    @click="$emit('screenshot')"
                    v-on="on"
                    depressed
                    block
                    color="white"
                    class="pa-0"
                  >
                    <template #default>
                      <v-icon>mdi-camera-plus-outline</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>Take a screenshot</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>

          <!-- Redact -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    depressed
                    toggle
                    block
                    color="white"
                    class="pa-0"
                    @click="redacted = !redacted"
                  >
                    <template #default>
                      <v-icon>{{redacted ? 'mdi-eye' : 'mdi-eye-off'}}</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>{{redacted ? 'Unredact' : "Redact"}} graph</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>

          <!-- Search -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    depressed
                    toggle
                    block
                    color="white"
                    class="pa-0"
                    @click="$emit('load')"
                  >
                    <template #default>
                      <v-icon>mdi-content-save-edit</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>Load saved query</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>

          <!-- Help -->
          <v-list-item class="pa-0">
            <v-fab-transition transition="scale-transition">
              <v-tooltip left>
                <template v-slot:activator="{ on }">
                  <v-btn
                    href="https://github.com/FSecureLABS/awspx/wiki/Data-Exploration"
                    target="_blank"
                    color="white"
                    class="pa-0"
                    v-on="on"
                    depressed
                    block
                  >
                    <template #default>
                      <v-icon>mdi-help-circle-outline</v-icon>
                    </template>
                  </v-btn>
                </template>
                <span>View help</span>
              </v-tooltip>
            </v-fab-transition>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: "Menu",

  data: function() {
    return {
      redacted: false,
      layout: {
        enabled: false,
        value: 0,
        values: ["Auto", "Grid", "Dagre", "Concentric"]
      }
    };
  },

  methods: {
    menu_item(item) {
      if ("active" in item) item.active = !item.active;
      item.fn();
    }
  },
  watch: {
    redacted(value) {
      this.$emit("redact", value);
    },
    "layout.value"(i) {
      this.$emit("update_layout", this.layout.values[i]);
    }
  }
};
</script>

<style>
.v-tooltip {
  z-index: 100;
}
.layout-options {
  position: absolute !important;
  font-size: 14px !important;
  right: 62px;
  width: 150px;
}
</style>



<template >
  <div id="autocomplete">
    <v-card flat class="ma-0 pa-2">
      <fieldset class="label" :class="active ? 'active' : ''">
        <legend class="mx-2">
          <span
            class="px-1"
            :style="{ opacity: disabled ? 0.4 : 1 }"
            :class="active ? 'primary--text' : ''"
            >{{ "label" in search ? search.label : "" }}</span
          >
        </legend>
        <v-autocomplete
          v-model="search.value"
          ref="autocomplete"
          :placeholder="'placeholder' in search ? search.placeholder : ' '"
          :menu-props="{ top: true, nudgeTop: 20, value: menu }"
          :class="disabled ? 'disabled' : ''"
          :search-input.sync="search.input"
          :aria-autocomplete="false"
          :disabled="disabled"
          :cache-items="false"
          :items="resources"
          :loading="loading"
          :filter="filter"
          @input="search.input = null"
          @click="menu = !menu"
          @focus="focus"
          @blur="blur"
          background-color="white"
          class="ma-0 pa-0 pb-2"
          item-text="name"
          item-value="id"
          return-object
          hide-details
          append-icon
          multiple
          rounded
        >
          <template #item="data">
            <TemplateSelectItem
              :width="width"
              :search="search.input"
              :data="data"
            />
          </template>

          <template #selection="data">
            <TemplateSelectSearch
              :data="data"
              close
              @add="select"
              @close="
                search.value = search.value.filter((s) => s.id !== data.item.id)
              "
            />
          </template>

          <!-- 'Any Resource' placeholder -->
          <template #prepend-inner>
            <div style="width: 0px" v-show="placeholder">
              <div v-show="placeholder_active" class="ml-1" style="width: 80px">
                <TemplateSelectSearch :data="any" />
              </div>
            </div>
          </template>

          <template v-slot:no-data>
            <v-list-item>
              <v-list-item-title class="font-italic font-weight-light"
                >No resources were found</v-list-item-title
              >
            </v-list-item>
          </template>

          <template #append>
            <v-tooltip top v-if="length > 0">
              <template v-slot:activator="{ on }">
                <v-btn
                  color="primary"
                  v-on="on"
                  @click="search.value = null"
                  icon
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
              <span>
                <b>Clear all</b>
              </span>
            </v-tooltip>

            <v-tooltip top v-if="append.enabled">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" v-on="on" @click="$emit('append')" icon>
                  <v-icon>{{ append.icon }}</v-icon>
                </v-btn>
              </template>
              <span>
                <b>{{ append.description }}</b>
              </span>
            </v-tooltip>
          </template>
        </v-autocomplete>
      </fieldset>
    </v-card>
  </div>
</template>


<script>
import icons from "@/icons.js";
import TemplateSelectSearch from "@/components/TemplateSelectSearch";
import TemplateSelectItem from "@/components/TemplateSelectItem";

export default {
  components: {
    TemplateSelectSearch,
    TemplateSelectItem,
  },
  props: {
    resources: {
      Type: Array,
      default: [],
    },
    search: {
      Type: Object,
      default: {},
    },
    loading: {
      Type: Boolean,
      default: false,
    },
    disabled: {
      Type: Boolean,
      default: false,
    },
    placeholder: {
      Type: Boolean,
      default: false,
    },
    width: {
      Type: String,
      default: "100%",
    },
    append: {
      Type: Object,
      default: () => {
        return { enabled: false };
      },
    },
  },
  data: function () {
    return {
      active: false,
      menu: false,
      length: 0,
      any: {
        item: {
          name: "Any",
          type: "AWS::Resource",
        },
        icons: icons,
      },
    };
  },
  methods: {
    select(event) {
      this.menu = false;
      this.$emit("add", event);
      this.$emit("select", event);
    },

    focus() {
      this.active = true;
    },
    blur() {
      this.search.input = null;
      this.active = false;
      this.menu = false;
    },
    filter(item, search, text) {
      this.menu = true;
      return [
        item.name,
        item.id,
        ...Object.keys(item.tags).map((k) => `${k}: ${item.tags[k]}`),
      ].some((k) => k.toLowerCase().includes(search.toLowerCase()));
    },
  },
  watch: {
    "search.value.length"(length) {
      this.length = length;
    },
  },
  computed: {
    placeholder_active() {
      return (
        this.placeholder && !this.menu && !this.active && this.length === 0
      );
    },
  },
};
</script>

<style>
.disabled {
  opacity: 0.4;
  background-color: whitesmoke;
}
.label {
  border: 0.5px solid rgba(0, 0, 0, 0.5);
  color: rgba(0, 0, 0, 0.5);
  border-radius: 4px 4px;
}
.label.active {
  border: 2px solid rgba(25, 118, 210, 0.7);
  color: rgba(25, 118, 210, 0.7);
  border-radius: 4px 4px;
}
</style>
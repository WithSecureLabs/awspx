<template >
  <div id="autocomplete">
    <v-autocomplete
      v-model="search.value"
      ref="autocomplete"
      :placeholder="'placeholder' in search ? search.placeholder : ' '"
      :menu-props="{top: true, nudgeTop: 10, value: menu}"
      :label="'label' in search ? search.label : ''"
      :class="disabled ? 'disabled' : ''"
      :search-input.sync="search.input"
      @input="search.input = null"
      background-color="white"
      :aria-autocomplete="false"
      class="ma-0 pa-0 my-3"
      @click="menu = !menu"
      :disabled="disabled"
      :cache-items="false"
      :items="resources"
      :loading="loading"
      :filter="filter"
      item-text="name"
      item-value="id"
      @focus="focus"
      return-object
      hide-details
      @blur="blur"
      append-icon
      clearable
      message=" "
      multiple
      outlined
    >
      <template #item="data">
        <TemplateSelectItem :width="width" :search="search.input" :data="data" />
      </template>

      <template #selection="data">
        <TemplateSelectSearch
          :data="data"
          close
          @close="search.value = search.value.filter(s => s.id !== data.item.id)"
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
          <v-list-item-title class="font-italic font-weight-light">No resources were found</v-list-item-title>
        </v-list-item>
      </template>

      <template #append>
        <v-tooltip top v-if="append.enabled">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" v-on="on" @click="$emit('append')" icon class="mt-n2">
              <v-icon>{{append.icon}}</v-icon>
            </v-btn>
          </template>
          <span>
            <b>{{append.description}}</b>
          </span>
        </v-tooltip>
      </template>
    </v-autocomplete>
  </div>
</template>


<script>
import icons from "@/icons.js";
import TemplateSelectSearch from "@/components/TemplateSelectSearch";
import TemplateSelectItem from "@/components/TemplateSelectItem";

export default {
  components: {
    TemplateSelectSearch,
    TemplateSelectItem
  },
  props: {
    resources: {
      Type: Array,
      default: []
    },
    search: {
      Type: Object,
      default: {}
    },
    loading: {
      Type: Boolean,
      default: false
    },
    disabled: {
      Type: Boolean,
      default: false
    },
    placeholder: {
      Type: Boolean,
      default: false
    },
    width: {
      Type: String,
      default: "100%"
    },
    append: {
      Type: Object,
      default: () => {
        return { enabled: false };
      }
    }
  },
  data: function() {
    return {
      active: false,
      menu: false,
      length: 0,
      any: {
        item: {
          name: "Any",
          type: "AWS::Resource"
        },
        icons: icons
      }
    };
  },
  methods: {
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
      return (
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        item.id.toLowerCase().includes(search.toLowerCase())
      );
    }
  },
  watch: {
    "search.value.length"(length) {
      this.length = length;
    }
  },
  computed: {
    placeholder_active() {
      return (
        this.placeholder && !this.menu && !this.active && this.length === 0
      );
    }
  }
};
</script>

<style>
.disabled {
  opacity: 0.4;
  background-color: whitesmoke;
}
</style>
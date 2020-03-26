     
<template >
  <div id="autocomplete">
    <v-autocomplete
      v-model="search.value"
      :placeholder="'placeholder' in search ? search.placeholder : ' '"
      :label="'label' in search ? search.label : ''"
      :menu-props="{top: true, nudgeTop: 10}"
      :search-input.sync="search.input"
      @click:append="$emit('append')"
      @input="search.input = null"
      background-color="white"
      :aria-autocomplete="false"
      class="ma-0 pa-0 my-3"
      :append-icon="append"
      :disabled="disabled"
      :cache-items="true"
      :class="classes()"
      :items="resources"
      :loading="loading"
      :filter="filter"
      item-text="name"
      item-value="id"
      return-object
      hide-details
      hide-no-data
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
          @close="search.value = search.value.filter(s => s.id !== data.item.id)"
        />
      </template>

      <template #prepend-inner>
        <div style="width: 0px" v-show="placeholder && search.value.length === 0">
          <div style="width: 77px">
            <TemplateSelectSearch :data="any" />
          </div>
        </div>
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
      Type: String,
      default: "$dropdown"
    }
  },
  data: function() {
    return {
      icons: icons,
      any: {
        item: {
          name: "Any",
          type: "AWS::Resource"
        }
      }
    };
  },
  methods: {
    filter(item, search, text) {
      return (
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        item.id.toLowerCase().includes(search.toLowerCase())
      );
    },
    classes() {
      const classes = [];

      if (this.disabled) classes.push("disabled");
      if (this.placeholder && this.search.value.length === 0)
        classes.push("empty");

      return classes.join(" ");
    }
  }
};
</script>

<style>
.empty.v-select.v-text-field input {
  padding-left: 77px;
}

.disabled {
  opacity: 0.4;
  background-color: whitesmoke;
}
</style>



<template>
  <v-list-item :style="{'max-width': width}" class="pa-0 ma-0">
    <v-list-item-avatar size="40" style="border: 1px solid #ccc; padding: 25px">
      <img height="40" width="40" :src="img(data.item)" />
    </v-list-item-avatar>
    <v-list-item-content style="text-align: center">
      <v-list-item-title v-html="highlight(data.item.name)"></v-list-item-title>
      <v-list-item-subtitle style="font-size: 12px">{{data.item.id}}</v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>


<script>
import icons from "@/icons.js";

export default {
  props: {
    data: {},
    search: "",
    width: {
      type: String,
      default: undefined
    }
  },
  data: function() {
    return { icons };
  },
  methods: {
    img(item) {
      return item.type.split("::").reduce((o, k) => {
        return Object.keys(o).includes(k) ? o[k] : this.icons.AWS.Resource;
      }, this.icons);
    },
    highlight(value) {
      if (typeof value !== "string" || value.length === 0) return value;
      const re = new RegExp(this.search, "gi");
      let v = value.replace("<b>", "").replace("</b>");
      Array.from(new Set(v.match(re))).map(
        m => (v = v.replace(m, `<b>${m}</b>`))
      );
      return v;
    }
  }
};
</script>

<style>
</style>
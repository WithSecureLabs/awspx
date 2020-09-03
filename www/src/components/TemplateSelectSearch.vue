<template >
  <v-chip
    v-on="data.on"
    :color="close ? '#484848' : '#696969'"
    @click:close="$emit('close')"
    :close="close"
    class="ma-0 mr-2"
    outlined
  >
    <v-avatar outlined>
      <v-img :src="img(data.item)" />
    </v-avatar>
    <div class="ml-2">
      <span class="item">{{ data.item.name }}</span>
    </div>
  </v-chip>
</template>

<script>
import icons from "@/icons.js";

export default {
  props: {
    data: {},
    close: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return { icons: icons };
  },
  methods: {
    img(item) {
      if (!Object.keys(item).includes("type")) return this.icons.AWS.Resource;

      return item.type.split("::").reduce((o, k) => {
        return Object.keys(o).includes(k) ? o[k] : this.icons.AWS.Resource;
      }, this.icons);
    }
  }
};
</script>

<style>
.item {
  font-size: 10px;
  max-width: 150px;
  display: block !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
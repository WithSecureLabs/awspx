<template >
  <v-chip
    @click:close="$emit('close')"
    v-on="data.on"
    class="ma-0"
    :color="close ? 'black' : ''"
    outlined
    :close="close"
  >
    <v-avatar outlined>
      <v-img :src="img(data.item)" />
    </v-avatar>
    <span class="ml-2 item">{{ data.item.name }}</span>
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

      return item.type
        .split("::")
        .reduce(
          (o, i) => (i in o ? o[i] : this.icons.AWS.Resource),
          this.icons
        );
    }
  }
};
</script>

<style>
.item {
  font-size: 11px;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}
</style>
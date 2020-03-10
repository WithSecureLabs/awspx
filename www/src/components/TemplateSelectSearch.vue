<template >
  <v-chip
    class="ma-0"
    @click:close="v.value = v.value.filter(s => s.id !== data.item.id)"
    v-on="data.on"
    outlined
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
    data: {}
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
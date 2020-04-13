<template>
  <v-dialog :value="enabled">
    <v-card>
      <!-- Resuls dialog controls -->
      <v-card-title>
        <v-text-field v-model="search" prepend-icon="mdi-magnify" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-btn small depressed fab color="white" @click="$emit('close')">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <!-- Results table -->
      <v-card-text>
        <v-data-table multi-sort :search="search" :headers="headers" :items="items">
          <template #body="{ items }">
            <tbody>
              <tr v-for="(item, i) in items" :key="i">
                <td class="text-left" v-for="(v, k) in item" :key="k">
                  <span
                    style="font-size: 12px; line-height: 1;"
                    v-html="results_highlight(v).replace(/ /g, '&nbsp;').replace(/\n/g, '<br>')"
                  ></span>
                </td>
              </tr>
            </tbody>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "SearchResultsTable",
  props: {
    data: {
      type: Array,
      default: []
    },
    enabled: {
      Type: Boolean,
      value: false
    }
  },

  data: function() {
    return {
      search: "",
      headers: [],
      items: []
    };
  },
  watch: {
    data(items) {
      // Recursively parses JSON strings to return a single object
      function json(j) {
        if (typeof j === "undefined" || j === null) return "";
        else if (Array.isArray(j)) j = j.map(k => json(k));
        else if (typeof j === "object")
          Object.keys(j).forEach(k => (j[k] = json(j[k])));
        else if (typeof j === "string")
          try {
            return json(JSON.parse(j));
          } catch (e) {
            return j;
          }
        return j;
      }

      // Update table headers and items
      this.headers =
        items.length > 0
          ? Object.keys(items[0]).map(h => {
              return { text: h.toString(), value: h.toString() };
            })
          : [];

      this.items = items.map(r => {
        Object.keys(r).forEach(k => {
          r[k] = r[k] === null ? r[k] : json(r[k]);
          if (typeof r[k] !== "string") {
            r[k] = `${JSON.stringify(r[k], null, 2)}`;
          }
        });
        return r;
      });

      this.search = "";
    }
  },
  methods: {
    results_highlight(html) {
      if (html.length === 0) return html;

      const re = new RegExp(this.search, "gi");
      let highlighted = html.replace("<b>", "").replace("</b>", "");
      Array.from(new Set(highlighted.match(re))).map(
        m => (highlighted = highlighted.split(m).join(`<b>${m}</b>`))
      );

      return highlighted;
    }
  }
};
</script>

<style >
.v-data-table thead {
  width: calc(100% - 1em);
}

.v-data-table thead,
tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.v-data-table tbody {
  display: block;
  height: calc(70vh);
  overflow: auto;
}

.v-data-table th {
  font-size: 13px !important;
  background-color: whitesmoke !important;
  color: black !important;
}

.v-data-table td {
  vertical-align: top;
}
.v-data-table tr td:nth-child(odd) {
  background: white;
}
.v-data-table tr td:nth-child(even) {
  background: #fbfbfb;
}
</style>

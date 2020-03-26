<template>
  <!-- Autocomplete -->
  <v-card class="search-filter" flat tile>
    <v-form v-model="valid" ref="form">
      <v-row>
        <!-- Selection -->
        <v-autocomplete
          placeholder="e.g. Either"
          v-model="selection"
          :items="selections"
          item-text="name"
          ref="selection"
          item-value="id"
          return-object
          :rules="rules"
          class="ma-2"
        >
          <template #selection="data">
            <TemplateSelectSearch :data="data" />
          </template>

          <template #item="data">
            <TemplateSelectItem :data="data" />
          </template>
        </v-autocomplete>

        <!-- Property-->
        <v-combobox
          placeholder="e.g. Name"
          v-model="property"
          :items="filter(properties, property)"
          :no-filter="true"
          :rules="rules"
          class="ma-2"
        ></v-combobox>

        <!-- Operator -->
        <v-select
          style="max-width: 80px"
          placeholder="e.g. ="
          v-model="operator"
          :cache-items="false"
          :items="operators"
          :rules="rules"
          class="ma-2"
        ></v-select>

        <!-- Value -->
        <v-combobox
          placeholder=" "
          :value="value"
          :no-filter="true"
          :items="filter(values, value)"
          :rules="rules"
          class="ma-2"
          @update:search-input="value = typeof $event === 'string' ? $event : '';"
        ></v-combobox>
      </v-row>
    </v-form>
  </v-card>
</template>

<script>
import TemplateSelectSearch from "@/components/TemplateSelectSearch";
import TemplateSelectItem from "@/components/TemplateSelectItem";

export default {
  name: "SearchFilter",
  components: { TemplateSelectSearch, TemplateSelectItem },
  props: {
    resources: {
      type: Array,
      default: []
    },
    actions: {
      type: Array,
      default: []
    },
    sources: {
      type: Array,
      default: []
    },
    targets: {
      type: Array,
      default: []
    },
    options: {
      actions: {
        type: Boolean,
        default: false
      },
      effective: {
        type: Boolean,
        default: false
      }
    },
    and: {
      type: Boolean,
      default: true
    },
    index: {
      type: Number,
      default: 0
    }
  },

  data: function() {
    return {
      valid: false,
      selection: {},
      property: "",
      operator: "",
      value: ""
    };
  },
  methods: {
    filter(options, search) {
      return options.filter(
        o =>
          o.length === 0 || o.toLowerCase().indexOf(search.toLowerCase()) >= 0
      );
    },

    validate() {
      this.$refs.form.validate();
    }
  },

  watch: {
    selection: "validate",
    property: "validate",
    operator: "validate",
    value: "validate",

    valid: function() {
      this.$emit("filter_update", {
        valid: this.valid
      });
    },

    text: () => {}
  },

  computed: {
    selections: function() {
      let selections = [
        { name: "Source" },
        { name: "Target" },
        { name: "Either", id: "Source OR Target" },
        { name: "Both", id: "Source AND Target" }
      ];

      if (this.options.actions) selections.unshift({ name: "Action" });

      if (selections.filter(s => s.name == this.selection.name).length === 0)
        this.selection = {};

      return selections.map((s, i) => {
        return {
          ...s,
          id: "id" in s ? s.id : undefined,
          type: s.name === "Action" ? "AWS::Action" : "AWS::Resource"
        };
      });
    },

    properties: function() {
      let properties = ["Name", "ID"];
      if ("element" in this.selection)
        properties = Object.keys(this.selection.element.data.properties).sort();
      else if (
        ["Source", "Target", "Either", "Both"].includes(this.selection.name)
      )
        properties = ["Name", "Arn", "TYPE", "ID"];
      else if (this.selection.name === "Action")
        properties = ["Name", "Effect", "Access", "Condition", "Description"];
      return properties;
    },

    operators: function() {
      let operators = ["="];
      if (["TYPE", "ID"].includes(this.property)) {
        this.operator = "=";
        operators = ["="];
      } else if (
        [
          "Name",
          "Arn",
          "Effect",
          "Access",
          "Condition",
          "Description"
        ].includes(this.property)
      ) {
        operators = ["=", "=~"];
      } else operators = ["=", "=~", ">", "<", ">=", "<="];
      return operators;
    },

    values: function() {
      let values = [];
      switch (this.operator) {
        case "=":
          if (this.property === "TYPE") {
            values = this.resources.map(r => [r.class, r.type]).flat();
            break;
          }

        case "=~":
          let properties = [];
          if (
            ["Either", "Both", "Source", "Target"].includes(this.selection.name)
          )
            properties = this.resources.map(r => r.element.data.properties);
          else if (this.selection.name === "Action") properties = this.actions;
          else
            properties = Object.keys(this.selection).includes("element")
              ? [this.selection.element.data.properties]
              : [];

          values = properties
            .filter(p => Object.keys(p).includes(this.property))
            .map(p => p[this.property]);

          break;

        default:
          break;
      }

      return Array.from(new Set(values)).sort();
    },

    rules() {
      const rules = [];

      if (
        typeof this.selection.name === "undefined" ||
        this.property === "" ||
        this.operator === "" ||
        this.value === ""
      ) {
        const rule = v =>
          (!!v && Object.keys(v).length > 0) || "field is mandatory";
        rules.push(rule);
      }

      if (this.property === "ID" && isNaN(this.value)) {
        const rule = v =>
          (v !== this.operator && v !== this.value) ||
          `invalid integer value for ID`;
        rules.push(rule);
      }

      if ([">", ">=", "<=", "<"].includes(this.operator) && isNaN(this.value)) {
        const rule = v =>
          (v !== this.operator && v !== this.value) ||
          `invalid operator/value combination`;
        rules.push(rule);
      }

      return rules;
    },

    text() {
      let text = [];

      if (this.valid) {
        let value = typeof this.value === "string" ? this.value : "";
        value = Number.isInteger(parseInt(value)) ? parseInt(value) : value;

        const names = [this.selection.name]
          .map(n =>
            ["Either", "Both"].includes(n) ? ["Source", "Target"] : [n]
          )
          .flat();

        switch (this.property) {
          case "TYPE":
            text = names.map(n => [`${n}:\`${value}\``]);
            break;

          case "ID":
            text = names.map(n => [`ID(${n})`, "=", value]);
            break;

          default:
            if ([">", ">=", "<=", "<"].includes(this.operator))
              text = names.map(n => [
                `${n}.${this.property}`,
                this.operator,
                this.value
              ]);
            else if (this.operator === "=~")
              text = names.map(n => [
                `${n}.${this.property}`,
                this.operator,
                `".*${this.value}.*"`
              ]);
            else
              text = names.map(n => [
                `${n}.${this.property}`,
                this.operator,
                Number.isInteger(parseInt(value)) ? value : `"${value}"`
              ]);

            break;
        }

        if (this.selection.name === "Both")
          text = text[0].concat("AND").concat(text[1]);
        else if (this.selection.name === "Either")
          text = ["(", ...text[0]].concat("OR").concat([...text[1], ")"]);
        else text = text[0];

        if (this.index > 0) text.unshift(this.and ? "AND" : "OR");
      }

      this.$emit("filter_update", {
        text: text.join(" ")
      });

      return text;
    }
  }
};
</script>

<style >
.search-filter .v-input input {
  font-size: 12px;
  /* font-style: italic; */
}
</style>

<template>
  <component :is="tag" :class="classlist">
    <slot></slot>
  </component>
</template>

<script>
export default {
  props: {
    size: {
      type: Number,
      require: false,
      default: 1,
    },
    alternative: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
  computed: {
    tag() {
      return `h${this.size}`;
    },
    classlist() {
      return ["heading", this.alternative ? "heading--alternative" : null];
    },
  },
};
</script>

<style lang="scss">
@import "../../assets/_variables.scss";

.heading {
  color: $blue;

  &--alternative {
    color: $black;
  }
}
</style>

<template>
  <component :is="tag" :href="toUrl ? toUrl : null" :class="classlist">
    <slot></slot>
  </component>
</template>

<script>
export default {
  props: {
    toUrl: {
      type: String,
      require: false,
      default: "",
    },
    alternative: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
  computed: {
    tag() {
      return this.toUrl ? "a" : "button";
    },
    classlist() {
      return ["button", this.alternative ? "button--alternative" : null];
    },
  },
};
</script>

<style lang="scss">
@import "../../assets/_variables.scss";

.button {
  background-color: $blue;
  color: white;
  padding: 10px 16px;
  font-weight: bold;
  box-shadow: 0 -8px 12px -16px hsla(0, 0%, 0%, 50%);

  &--alternative {
    padding: 8px 12px;
    font-size: 0.8rem;
    background-color: black;
  }
}
</style>

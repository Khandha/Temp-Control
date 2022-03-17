<template>
  <p :class="classlist">
    <slot></slot>
  </p>
</template>

<script>
export default {
  props: {
    alternative: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
  computed: {
    classlist() {
      return ["paragraph", this.alternative ? "paragraph--alternative" : null];
    },
  },
};
</script>

<style lang="scss">
.paragraph {
  color: hsl(0, 0%, 10%);

  &--alternative {
    font-size: 0.8rem;
  }
}
</style>

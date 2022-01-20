<template>
  <component :is="tag" :class="classList">
    <AppHeading v-if="heading" :alternative="true" :size="headingSize">
      {{ heading }}
    </AppHeading>
    <slot></slot>
  </component>
</template>

<script>
import AppHeading from "@/components/atoms/AppHeading";
export default {
  name: "AppBaseWrapper",
  components: { AppHeading },
  props: {
    heading: {
      type: String,
      require: false,
      default: null,
    },
    headingSize: {
      type: Number,
      require: false,
      default: 1,
    },
    solid: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
  computed: {
    tag() {
      return this.heading ? "section" : "div";
    },
    classList() {
      return [
        "container",
        "container--wrapper",
        this.solid ? "container--wrapper-solid" : null,
      ];
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  width: 100%;

  &--wrapper {
    padding: 16px 12px;

    &-solid {
      border-radius: 16px;
      background-color: white;
    }
  }
}
</style>

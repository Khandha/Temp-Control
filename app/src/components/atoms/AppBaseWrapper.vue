<template>
  <component :is="tag" :class="classList">
    <AppHeading v-if="headingSize" :alternative="true" :size="headingSize">
      <slot name="heading"></slot>
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
    headingSize: {
      type: Number,
      require: false,
      default: null,
    },
    solid: {
      type: Boolean,
      require: false,
      default: false,
    },
  },
  computed: {
    tag() {
      return this.headingSize ? "section" : "div";
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

<template>
  <teleport to="#app">
    <AppBaseWrapper
      heading="Settings"
      :heading-size="2"
      class="container--modal"
      :solid="true"
    >
      <p>asdasgfdfgvfsdaewrgsdcxf</p>
      <AppButton @click="closeSettings">Close</AppButton>
    </AppBaseWrapper>
  </teleport>
</template>

<script>
import AppBaseWrapper from "@/components/atoms/AppBaseWrapper";
import AppButton from "@/components/atoms/AppButton";
export default {
  name: "Settings",
  components: { AppButton, AppBaseWrapper },
  methods: {
    closeSettings() {
      this.$router.back();
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  &--modal {
    justify-content: space-between;
    width: 80%;
    min-height: 40%;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 100vh hsla(0, 0%, 0%, 30%);
    z-index: 9999;
  }
}
</style>

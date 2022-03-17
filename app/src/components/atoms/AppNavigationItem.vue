<template>
  <li class="navigation__item">
    <router-link :to="routePath" class="navigation__link">
      <img
        class="navigation__icon"
        :src="require('@/assets/' + iconName + '.svg')"
        alt="Icon"
      />
      <span class="navigation__label">{{ label }}</span>
    </router-link>
  </li>
</template>

<script>
export default {
  name: "AppNavigationItem",
  props: {
    iconName: {
      type: String,
      require: true,
    },
    label: {
      type: String,
      require: true,
    },
    routePath: {
      type: String,
      require: true,
    },
  },
  data() {
    return {
      icons: {
        home: "@/assets/home.svg",
        pieChart: "@/assets/pie-chart.svg",
        settings: "@/assets/settings.svg",
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.navigation {
  &__item {
    width: 100%;
    height: 100%;
  }

  &__link {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 108%;
    bottom: 20%;
    text-align: center;
    position: relative;
    overflow: hidden;
    z-index: 1;

    &--active {
      .navigation__icon {
        transform: translateY(0);
        opacity: 1;
        filter: invert(1) contrast(2);
        margin-top: 0;
      }

      .navigation__label {
        transform: translateY(0);
        opacity: 1;
      }
    }
  }

  &__icon {
    width: 26px;
    height: 26px;
    margin: 12px auto 0;
    pointer-events: none;
    transform: translateY(140%);
    opacity: 1;
    transition: ease 0.8s;
  }

  &__label {
    opacity: 0;
    margin-top: 20px;
    transform: translateY(70%);
    pointer-events: none;
    transition: ease 0.6s;
  }
}
</style>

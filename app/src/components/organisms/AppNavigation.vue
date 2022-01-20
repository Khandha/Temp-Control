<template>
  <nav class="container container--navigation">
    <ul class="navigation">
      <AppNavigationItem
        v-for="item in navItems"
        :key="item.id"
        :icon-name="item.icon"
        :label="item.label"
        :route-path="item.routePath"
        ref="navItem"
      />
    </ul>
    <span class="navigation__indicator" ref="navIndicator"></span>
  </nav>
</template>

<script>
import AppNavigationItem from "@/components/atoms/AppNavigationItem";

export default {
  name: "AppNavigation",
  components: { AppNavigationItem },
  data() {
    return {
      navItems: [
        {
          id: 0,
          label: "Dashboard",
          icon: "home",
          routePath: "/",
        },
        {
          id: 1,
          label: "Stats",
          icon: "pie-chart",
          routePath: "/stats",
        },
        {
          id: 2,
          label: "Settings",
          icon: "settings",
          routePath: "/settings",
        },
      ],
    };
  },
  methods: {
    getIndicatorOffset: (leftOffset, itemWidth, indicatorWidth) =>
      leftOffset + (itemWidth - indicatorWidth) / 2,

    setIndicator(targetId) {
      const { offsetLeft: leftOffset, offsetWidth: itemWidth } =
        this.$refs.navItem[targetId].$el;
      const indicatorWidth = this.$refs.navIndicator.offsetWidth;

      const indicatorOffset = this.getIndicatorOffset(
        leftOffset,
        itemWidth,
        indicatorWidth
      );

      this.$refs.navIndicator.style.transform = `translateX(${indicatorOffset}px)`;
    },
  },
  computed: {
    idFromRoute() {
      return this.navItems.find((item) => this.$route.name === item.label).id;
    },
  },
  mounted() {
    this.$router.afterEach(() => {
      this.setIndicator(this.idFromRoute);
    });
  },
  updated() {
    this.mounted();
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/_variables.scss";

.container {
  &--navigation {
    width: 100%;
    padding: 0 12px;
    position: absolute;
    left: 0;
    bottom: 0;
    background-color: $gray500;
    height: 82px;
  }
}

.navigation {
  display: flex;
  align-self: center;
  justify-content: space-between;
  flex-direction: row;
  width: 100%;
  height: 100%;

  &__indicator {
    width: 116px;
    height: 100%;
    position: absolute;
    z-index: 0;
    left: 0;
    transition: ease 0.5s;
    transform: translateX(-92px);

    &::before {
      content: "";
      border-radius: 50%;
      width: 55%;
      aspect-ratio: 1/1;
      position: absolute;
      left: 22.5%;
      top: -43%;
      z-index: 1;
      background-color: $blue;
    }

    &::after {
      content: "";
      background-color: $gray300;
      mask: url("../../assets/indicator-background.svg") top / contain no-repeat;
      position: absolute;
      width: 100%;
      height: 100%;
    }
  }
}
</style>

<template>
  <div class="content">
    <AppNavigation />
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import AppNavigation from "@/components/organisms/AppNavigation";
export default {
  components: { AppNavigation },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap");
@import "assets/_variables.scss";

.hidden {
  display: none;
}

@keyframes pop-in {
  from {
    opacity: 0;
    transform: translateY(-100px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0px) scale(1);
  }
}

main {
  animation: pop-in 0.4s cubic-bezier(.61,.35,.46,.91);
}

*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

button,
input {
  border: none;
  background: transparent;
  font-family: inherit;
  outline: none;
}

ul,
ol {
  list-style: none;
}

a {
  text-decoration: none;
  color: inherit;
}

body {
  font: 16px/32px normal, Poppins, sans-serif;
  color: $gray100;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100vw;
  height: 100vh;
}

#app {
  width: 100%;
  height: 100%;

  padding: 5vw;
  margin: 0 auto;

  @media screen and (min-width: 1200px) {
    width: 1200px
  }
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  &--main {
    width: 100%;
    padding: 6px 8px 88px;
  }
}

.content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

  height: 100%;
  aspect-ratio: 9/19.5;

  position: relative;
  margin: 0 auto;

  border-radius: 18px;
  background-color: $gray300;

  overflow: hidden;

  @media screen and (min-width: 1200px) {
    width: 100%;
    height: auto;

    aspect-ratio: 16/10;
  }
}
</style>

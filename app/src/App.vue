<template>
  <AppNavigation />
  <router-view :key="$route.path"></router-view>
</template>

<script>
import axios from "axios";
import AppNavigation from "@/components/organisms/AppNavigation";
export default {
  components: { AppNavigation },
  mounted() {
    axios
      .post("http://127.0.0.1:5000/settemp?temp=17")
      .then((res) => console.log(res.status));
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap");
@import "assets/_variables.scss";

.hidden {
  display: none;
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
  display: flex;
  align-items: center;
  justify-content: center;
  width: 347px;
  aspect-ratio: 9/19.5;
  flex-direction: column;
  background-color: $gray300;
  position: relative;
  overflow: hidden;
  border-radius: 18px;

  @media screen and (min-width: 946px) {
    width: 90%;
    aspect-ratio: 16/10;
  }
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  &--main {
    width: 100%;
    padding: 6px 8px 88px;

    @media screen and (min-width: 946px) {
      display: grid;
      grid-template-columns: 35% 65%;
      grid-template-rows: 82px auto;
    }
  }
}
</style>

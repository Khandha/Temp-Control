<template>
  <main class="container container--main">
    <header>
      <AppHeading :alternative="true">TempControl</AppHeading>
    </header>
    <AppBaseWrapper
      v-if="!isFetching"
      :solid="true"
      class="container--dashboard"
    >
      <TemperatureControl
        :initial-temperature="temperature.fetched"
        @temp-change="handleTemperatureChange"
      />
      <div class="summary">
        <div class="summary__item">
          <AppParagraph class="summary__label"
            >Current temperature:</AppParagraph
          >
          <span class="summary__value"
            >{{ temperature.fetched ? temperature.fetched : "- " }}°C</span
          >
        </div>
        <div class="summary__item">
          <AppParagraph class="summary__label">Given temperature:</AppParagraph>
          <span class="summary__value">{{
            temperature.given ? temperature.given + "°C" : "-"
          }}</span>
        </div>
        <div class="summary__item">
          <AppParagraph class="summary__label"
            >Estimated heat time:</AppParagraph
          >
          <span class="summary__value">{{
            estimatedTime ? estimatedTime : "-"
          }}</span>
        </div>
      </div>
    </AppBaseWrapper>
  </main>
</template>

<script>
import AppHeading from "@/components/atoms/AppHeading";
import AppBaseWrapper from "@/components/atoms/AppBaseWrapper";
import TemperatureControl from "@/components/organisms/TemperatureControl";
import AppParagraph from "@/components/atoms/AppParagraph";
import axios from "axios";

export default {
  name: "Dashboard",
  components: { AppParagraph, TemperatureControl, AppBaseWrapper, AppHeading },
  data() {
    return {
      isFetching: true,
      temperature: {
        fetched: null,
        given: null,
      },
      estimatedTime: null,
    };
  },
  methods: {
    setTemperature: (temperature) =>
      axios.post("http://127.0.0.1:5000/settemp?temp=" + temperature),
    getEstimatedTime: async (current, given) => {
      const {
        data: { "time-estimate": estimatedTime },
      } = await axios.get(
        `http://127.0.0.1:5000/estimate?current_temp=${current}&set_temp=${given}`
      );
      const timeData = estimatedTime.slice(0, -3).split(":");
      if (timeData) {
        return `${timeData[0]}h ${timeData[1]}m`;
      }
    },
    handleTemperatureChange(payload) {
      this.temperature.given = payload;
      this.setTemperature(payload);
      this.getEstimatedTime(
        this.temperature.fetched,
        this.temperature.given
      ).then((estimatedTime) => (this.estimatedTime = estimatedTime));
    },
  },
  async mounted() {
    const {
      data: { roomtemp: roomTemperature },
    } = await axios.get("http://127.0.0.1:5000/data");
    if (roomTemperature) {
      this.isFetching = !this.isFetching;
      this.temperature.fetched = Math.floor(roomTemperature);
    }
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/variables";

.container {
  &--main {
    align-items: center;
    width: 100%;
    height: 100%;
    padding: 6px 8px 88px;
    justify-content: space-evenly;
  }

  &--dashboard {
    height: 65%;
  }
}

.summary {
  margin-top: -25%;

  &__item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid $gray300;
    padding: 12px 0;

    &:last-of-type {
      border-bottom: 0;
    }
  }

  &__value {
    border-radius: 8px;
    padding: 2px 8px;
    color: white;
    font-weight: bold;
    background-color: $gray150;
  }
}

header {
  height: 15%;
}
h1 {
  font-size: 180%;
}
</style>

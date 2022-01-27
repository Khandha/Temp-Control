<template>
  <main class="container container--main">
    <header>
      <AppHeading :alternative="true">TempControl</AppHeading>
    </header>
    <TemperatureControl
        v-if="!isFetching"
        :initial-temperature="temperature.setPoint"
        @temp-change="handleTemperatureChange"
    />
    <AppBaseWrapper
      :solid="true"
    >
      <ul class="summary">
        <li class="summary__item">
          <AppParagraph class="summary__label">
            Current temperature:
          </AppParagraph>
          <AppSummaryValue :value="temperature.current" />
        </li>
        <li class="summary__item">
          <AppParagraph class="summary__label">
            Given temperature:
          </AppParagraph>
          <AppSummaryValue :value="temperature.given" />
        </li>
        <li class="summary__item">
          <AppParagraph class="summary__label">
            Estimated time:
          </AppParagraph>
          <div class="rzyg-totalny">
            <AppButton :alternative="true" @click="toggleFrame" :disabled="!frameUrl">Estimation graph</AppButton>
            <AppSummaryValue :value="estimatedTime" />
          </div>
        </li>
      </ul>
    </AppBaseWrapper>
  </main>
  <div v-if="isFrameVisible" class="frame-masakra-wrapper">
    <iframe height="400" width="500" src="https://google.com"></iframe>
    <AppButton @click="toggleFrame">Close graph</AppButton>
  </div>
</template>

<script>
import AppHeading from "@/components/atoms/AppHeading";
import AppBaseWrapper from "@/components/atoms/AppBaseWrapper";
import TemperatureControl from "@/components/organisms/TemperatureControl";
import AppParagraph from "@/components/atoms/AppParagraph";
import AppButton from "@/components/atoms/AppButton";
import axios from "axios";
import AppSummaryValue from "@/components/atoms/AppSummaryValue";

export default {
  name: "Dashboard",
  components: {AppSummaryValue, AppParagraph, TemperatureControl, AppBaseWrapper, AppHeading, AppButton },
  data() {
    return {
      isFetching: true,
      temperature: {
        current: null,
        given: null,
        setPoint: null,
      },
      estimatedTime: null,
      isFrameVisible: false,
      frameUrl: null,
    };
  },
  methods: {
    toggleFrame() {
      this.isFrameVisible = !this.isFrameVisible
    },
    setTemperature: temperature =>
      axios.post("http://127.0.0.1:5000/settemp?temp=" + temperature),
    getEstimatedTime: async (current, given) => {
      const { data: {
        "time-estimate": estimatedTime
      } } = await axios.get(
          `http://127.0.0.1:5000/estimate?current_temp=${current}&set_temp=${given}`
      )
      const timeData = estimatedTime.slice(0, -3).split(":");
      return `${timeData[0]}h ${timeData[1]}m`;
    },
    getFrameUrl: async (current, given) => {
      const { data } = await axios.get(
          `http://127.0.0.1:5000/data/chart_generate?current_temp=${current}&set_temp=${given}`
      )
      console.log(data);
    },
    async handleTemperatureChange(payload) {
      this.temperature.given = payload;

      await this.setTemperature(payload);

      this.estimatedTime = await this.getEstimatedTime(
        this.temperature.current,
        this.temperature.given
      );
      this.getFrameUrl(
          this.temperature.current,
          this.temperature.given
      )
    },
  },
  mounted() {
    axios.get("http://127.0.0.1:5000/data").then(({ data }) => {
      const {
        set_point: setPoint,
        roomtemp: roomTemperature
      } = data;
      this.isFetching = !this.isFetching;
      this.temperature.setPoint = Math.floor(setPoint);
      this.temperature.current = Math.floor(roomTemperature);
    });
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/variables";

.container--main {
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 6px 8px 88px;
  justify-content: center;
}

.summary {
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
  padding: 30px 0;
}
h1 {
  font-size: 180%;
}

.rzyg-totalny {
  display: flex;
  justify-content: space-between;

  button {
    margin-right: 16px;
    transition: all 0.5s ease-in ;

    &:disabled {
      opacity: 0.15;
    }
  }
}

.frame-masakra-wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 10vw solid rgba(0,0,0,0.3);
  z-index: 99999;

  iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  button {
    margin-left: 25%;
    width: 50%;
  }
}
</style>

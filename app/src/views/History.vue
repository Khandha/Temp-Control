<template>
  <main class="container container--main">
    <div class="button-wrapper">
      <AppButton @click="setChartData('three')">Last 3 hours</AppButton>
      <AppButton @click="setChartData('six')">Last 6 hours</AppButton>
      <AppButton @click="setChartData('twelve')">Last 12 hours</AppButton>
    </div>
    <AppParagraph>This section allows you to see the history of heater's work based on last few hours.</AppParagraph>
    <AppBaseWrapper
        :solid="true"
        class="chart-mam-dosc"
    >
      <apexchart type="line" :options="options" :series="series" ref="chart2"/>
    </AppBaseWrapper>
  </main>
</template>

<script>
import AppBaseWrapper from "@/components/atoms/AppBaseWrapper";
import AppButton from "@/components/atoms/AppButton";
import axios from "axios";
import AppParagraph from "@/components/atoms/AppParagraph";
export default {
  name: "History",
  components: {AppParagraph, AppButton, AppBaseWrapper},
  data() {
    return {
      options: {
        chart: {
          id: "zabij-mnie-echhh",
          width: "100%",
          height: "100%",
          toolbar: {
            show: false,
          },
        },
        xaxis: {
          type: "category",
          dateTimeUTC: true,
          categories: [],
          labels: {
            show: false,
            format: "HH:mm:ss",
          },
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          }
        },
      },
      series: [
        {
          name: "Room temperature",
          data: [],
        },
        {
          name: "Heater temperature",
          data: [],
        },
      ],
    };
  },
  methods: {
    async setChartData(arg) {
      await this.getTemperature(arg);
    },
    parseTime: (time) => new Date("2019-01-19T" + time).getTime(),
    async getTemperature(plotSize) {
      let {
        data
      } = await axios.get(
          "http://127.0.0.1:5000/data/" + plotSize
      );
      const roomTemp = data.reduce((acc, { roomtemp }, index) => ([
        ...acc,
        {x: index, y: roomtemp.toFixed(2)}
      ]), []);
      const heaterTemp = data.reduce((acc, { heatertemp }, index) => ([
        ...acc,
        {x: index, y: heatertemp.toFixed(2)}
      ]), []);
      console.log(roomTemp, heaterTemp);
      this.$refs.chart2.updateSeries([{data: roomTemp},{data: heaterTemp}]);
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
p {
  text-align: center;
  padding: 15px 0;
  width: 50%;
  margin: 0 auto;
}

.chart-mam-dosc {
  width: 55%;
  margin: 0 auto;
}
.button-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  width: 100%;
  padding: 15px 10px;
}
</style>

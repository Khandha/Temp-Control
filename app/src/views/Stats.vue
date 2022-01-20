<template>
  <main class="container container--main" ref="viewport">
    <h1>Stats here</h1>
    <AppBaseWrapper :solid="true">
      <apexchart type="line" :options="options" :series="series" />
    </AppBaseWrapper>
  </main>
</template>

<script>
import AppBaseWrapper from "@/components/atoms/AppBaseWrapper";
import axios from "axios";

export default {
  name: "Stats",
  components: { AppBaseWrapper },
  data() {
    return {
      options: {
        chart: {
          id: "vuechart-example",
          width: "100%",
          toolbar: {
            show: false,
          },
        },
        xaxis: {
          type: "datetime",
          dateTimeUTC: true,
          categories: [],
          labels: {
            show: true,
            format: "HH:mm:ss",
          },
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
    parseTime: (time) => new Date("2019-01-19T" + time).getTime(),
    async getTemperature(plotSize) {
      const { data } = await axios.get(
        "http://127.0.0.1:5000/data/more?count=" + plotSize
      );
      console.log(data);
      data.forEach(({ time, roomtemp, heatertemp }, index) => {
        const roomTemp = roomtemp.toFixed(2);
        const heaterTemp = heatertemp.toFixed(2);
        setTimeout(() => {
          const seriesSize = this.series[0].data.length;

          if (seriesSize === 20) {
            this.series[0].data.splice(0, 1);
            this.series[1].data.splice(0, 1);
            this.options.xaxis.categories.splice(0, 1);
          }

          this.series[0].data.push(roomTemp);
          this.series[1].data.push(heaterTemp);
          this.options.xaxis.categories.push(this.parseTime(time));

          console.log(index, seriesSize, data.length);
          data.splice(0, 1);
        }, 1000 * index++);
      });
    },
  },
  created() {
    this.getTemperature(50);
  },
};
</script>

<style scoped>
h1 {
  font-size: 180%;
}
</style>

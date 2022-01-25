<template>
  <main class="container container--main" ref="viewport">
    <AppBaseWrapper :solid="true" class="container--chart">
      <apexchart type="line" :options="options" :series="series" ref="chart"/>
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
          id: "chart",
          width: "100%",
          height: "100%",
          toolbar: {
            show: false,
          },
          animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
              speed: 1000
            }
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

      data.forEach(({ time, roomtemp, heatertemp }, index) => {
        const roomTemp = roomtemp.toFixed(2);
        const heaterTemp = heatertemp.toFixed(2);
        setInterval(() => {
          //const seriesSize = this.series[0].data.length;

          // this.series[0].data.push(roomTemp);
          // this.series[1].data.push(heaterTemp);
          //this.options.xaxis.categories.push(this.parseTime(time));

          this.$refs.chart.updateSeries([{
            data: [{
              x: this.parseTime(time),
              y: roomTemp
            }, {
              x: this.parseTime(time),
              y: heaterTemp
            }]
          }])
        }, 1000 * index++);
      });
    },
  },
  created() {
    setInterval(() => {
      this.getTemperature(50);
    }, 50000);
  },
};
</script>

<style lang="scss" scoped>
.container--chart {
  width: 75%;
  grid-area: 1 / 1 / 3 / 3;
  justify-self: center;
}
</style>

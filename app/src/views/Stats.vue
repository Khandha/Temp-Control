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
var roomTempData = [];
var heaterTempData = []
var TICKCOUNT = 15

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
          range: TICKCOUNT * 1000,
          labels: {
            show: true,
            format: "HH:mm:ss",
          },
        },
        yaxis: {
          min: 10,
          max: 45,
          tickAmount: 20,
          labels: {
            formatter: function(val) {
              return val.toFixed(0)
            }
          }
        },
        stroke: {
          curve: "smooth"
        },
      },
      series: [
        {
          name: "Room temperature",
          data: roomTempData.slice(),
        },
        {
          name: "Heater temperature",
          data: heaterTempData.slice(),
        },
      ],
    };
  },
  methods: {
    parseTime: (time) => new Date("2019-01-19T" + time).getTime(),
    async fill() {
      let { data } = await axios.get(
        "http://127.0.0.1:5000/data/more?count=" + TICKCOUNT * 2
      );
      data = data.slice().reverse();
      for(let i = 0; i < TICKCOUNT; i++) {
        roomTempData.push({x: this.parseTime(data[i].time), y: data[i].roomtemp.toFixed(2)})
        heaterTempData.push({x: this.parseTime(data[i].time), y: data[i].heatertemp.toFixed(2)})
      }
      // console.log(roomTempData);
      this.$refs.chart.updateSeries([{
        data: roomTempData
        }, {
          data: heaterTempData
        }], 1000);

      await this.getTemperature(TICKCOUNT);

      setInterval(() => {
        this.getTemperature(TICKCOUNT);
      }, TICKCOUNT * 1000);

      setInterval(function () {
        this.clean()
      }, 60000)

    },
    async clean() {
      roomTempData.splice(0, roomTempData.length - TICKCOUNT + 2)
      heaterTempData.splice(0, heaterTempData.length - TICKCOUNT + 2)
      this.$refs.chart.updateSeries([{
          data: roomTempData
        }, {
          data: heaterTempData
        }], 1000);
      },
    async getTemperature(plotSize) {
      let { data } = await axios.get(
        "http://127.0.0.1:5000/data/more?count=" + plotSize
      );
      data = data.slice().reverse();
      data.forEach(({ time, roomtemp, heatertemp }, index) => {
        const roomTemp = roomtemp.toFixed(2);
        const heaterTemp = heatertemp.toFixed(2);
        setTimeout(() => {
          if (!roomTempData.some(e => e.x === this.parseTime(time))) {
            roomTempData.push({x: this.parseTime(time), y: roomTemp});
            heaterTempData.push({x: this.parseTime(time), y: heaterTemp});
            if (roomTempData.length > TICKCOUNT) {
              for (let i = 0; i < roomTempData.length - (TICKCOUNT + 2); i++) {
                heaterTempData[i].y = 0;
                roomTempData[i].y = 0;
              }
            }
            this.$refs.chart.updateSeries([{
              data: roomTempData
            }, {
              data: heaterTempData
            }], 1000);
            console.log(roomTemp, heaterTemp, time);
          }
        }, 1000 * index++);
      });
    },
  },
  created() {
    this.fill();
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

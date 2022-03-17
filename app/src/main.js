import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";

import VueApexCharts from "vue3-apexcharts";

const app = createApp(App);

app.use(router);
app.use(VueApexCharts);
app.mount("#app");

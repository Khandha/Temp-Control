import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "@/views/Dashboard";
import Stats from "@/views/Stats";
import History from "@/views/History";

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/stats",
    name: "Stats",
    component: Stats,
  },
  {
    path: "/history",
    name: "History",
    component: History,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: "navigation__link--active",
});

export default router;

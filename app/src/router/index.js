import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "@/views/Dashboard";
import Stats from "@/views/Stats";
import Settings from "@/views/Settings";

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
    path: "/settings",
    name: "Settings",
    component: Settings,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: "navigation__link--active",
});

export default router;

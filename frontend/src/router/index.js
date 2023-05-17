import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },

  {
    path: "/loginsignup",
    name: "loginsignup",
    component: () => import("../components/LoginSignup.vue"),
  },
  {
    path: "/",
    name: "start",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/StartView.vue"),
  },
  {
    path: "/postblog",
    name: "postblog",
    component: () => import("../components/PostBlog.vue"),
  },
  {
    path: "/editblog/:id",
    name: "editblog",
    component: () => import("../components/EditBlog.vue"),
  },

  {
    path: "/postengage/:id",
    name: "postengage",
    component: () => import("../components/PostEngage.vue"),
  },
  {
    path: "/readblog/:id",
    name: "readblog",
    component: () => import("../components/ReadBlog.vue"),
  },
  {
    path: "/profile/:username",
    name: "profile",
    component: () => import("../components/UserProfile.vue"),
  },
  {
    path: "/editprofile",
    name: "editprofile",
    component: () => import("../components/EditProfile.vue"),
  },
  {
    path: "/searchuser",
    name: "searchuser",
    component: () => import("../components/SearchUser.vue"),
  },
  {
    path: "/comment/:id",
    name: "commentblog",
    component: () => import("../components/CommentBlog.vue"),
  },
  {
    path: "/followers",
    name: "followers",
    component: () => import("../components/MyFollowers.vue"),
  },
  {
    path: "/followings",
    name: "followings",
    component: () => import("../components/MyFollowings.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

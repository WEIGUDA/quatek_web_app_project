<template>
  <div id="app">
    <AppHeader></AppHeader>
    <router-view/>
    <AppFooter></AppFooter>
  </div>
</template>

<script>
import Header from "@/components/Header";
import Footer from "@/components/Footer";
// import axios from 'axios';
import { mapActions } from "vuex";
export default {
  components: {
    AppHeader: Header,
    AppFooter: Footer
  },
  methods: {
    ...mapActions(["init_jwt_token", "logout"])
  },
  created() {
    this.init_jwt_token();
  },
  destroyed() {
    this.logout();
  }
};
</script>


<style>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
#app {
  font-family: "Helvetica Neue", Helvetica, Arial, "STXihei", "Hiragino Sans GB",
    "Microsoft YaHei", sans-serif;
}

@media (min-width: 576px) {
}

/*  Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
}

/*  Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
}

/*  Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
}
</style>

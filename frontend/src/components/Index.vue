<template>
  <div class="container">
    <p class="text-center">ESD 检测门禁系统</p>
  </div>
</template>

<script>
export default {
  name: "index",
  data: function() {
    return {};
  },
  props: {},
  components: {}
};
</script>

<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
p {
  background-color: #009766;
  font-size: 200%;
  color: #ffffff;
  height: 180px;
  margin: 150px 0;
  padding: 65px 0;
}

/*  Small devices (landscape phones, 576px and up) */
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
  p {
    padding: 70px 0;
    height: 230px;
    margin: 200px 0;
    font-size: 400%;
  }
}
</style>

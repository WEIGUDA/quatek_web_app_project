<template>
  <div class="container-fluid">
    <div class="row">
      <b-nav vertical class="col-2 offset-1 sidebar">
        <b-nav-item :to="{name: 'system-config'}">系统设置</b-nav-item>
        <b-nav-item :to="{name: 'interval-task'}">任务设置(按间隔)</b-nav-item>
        <b-nav-item :to="{name: 'crontab-task'}">任务设置(按日期)</b-nav-item>
      </b-nav>

      <div class="col-9">
        <router-view></router-view>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  methods: {},
};
</script>

<style scoped>
.container-fluid {
  min-height: 500px;
}
.sidebar a {
  color: #059c66;
}
.sidebar a.active {
  /* color: white; */
  background-color: #e9ecef;
}
</style>

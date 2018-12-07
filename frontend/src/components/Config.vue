<template>
  <div class="container-fluid">
    <div class="row">
      <b-nav vertical class="col-md-2 offset-md-1 sidebar">
        <b-nav-item :to="{name: 'system-config'}" key="system-config">Email&SMTP设置</b-nav-item>
        <b-nav-item :to="{name: 'other-database'}" key="other-database">其他数据库</b-nav-item>
        <b-nav-item :to="{name: 'interval-task'}" key="interval-task">任务设置(按间隔)</b-nav-item>
        <b-nav-item :to="{name: 'crontab-task'}" key="crontab-task">任务设置(按日期)</b-nav-item>
        <b-nav-item :to="{name: 'background-task'}" key="background-task">管理员工具</b-nav-item>
        <b-nav-item :to="{name: 'class-time-config'}" key="class-time-config">班别设置</b-nav-item>
        <b-nav-item
          :to="{name: 'card_number_convertor_config'}"
          key="card_number_convertor_config"
        >卡号转换工具</b-nav-item>
        <br>
      </b-nav>

      <div class="col-md-9">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {}
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

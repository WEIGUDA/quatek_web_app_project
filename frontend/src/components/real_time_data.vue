<template>
  <div class="container">
    <table class="table">
      <tr>
        <td>Log ID</td>
        <td>卡片号码</td>
        <td>姓名</td>
        <td>工号</td>
        <td>卡片分类</td>
        <td>进出标志</td>
        <td>MC ID</td>
        <td>测试时间</td>
        <td>测试结果</td>
        <td>是否测试</td>
        <td>手测试值</td>
        <td>左脚测试值</td>
        <td>右脚测试值</td>
      </tr>
      <tr v-for="log in get_logs" :key="log.log_id">
        <td>{{log.log_id}}</td>
        <td>{{ log.card_number }}</td>
        <td>{{ log.name }}</td>
        <td>{{ log.job_number }}</td>
        <td>{{ log.card_category }}</td>
        <td>{{ log.in_out_symbol }}</td>
        <td>{{ log.mc_id }}</td>
        <td>{{ log.test_datetime | moment('YYYY-MM-DD HH:mm:ss') }}</td>
        <td>{{ log.test_result }}</td>
        <td>{{ log.is_tested }}</td>
        <td>{{ log.hand }}</td>
        <td>{{ log.left_foot }}</td>
        <td>{{ log.right_foot }}</td>
      </tr>
    </table>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      //
    };
  },
  computed: {
    ...mapGetters(["get_logs"])
  }
};
</script>

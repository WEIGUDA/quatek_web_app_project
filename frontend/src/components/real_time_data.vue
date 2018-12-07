<template>
  <div class="container">
    <p
      v-for="log in get_logs"
      :key="log.log_id"
    >Log ID: {{log.log_id}}, 卡片号码: {{ log.card_number }}, 姓名: {{ log.name }}, 工号: {{ log.job_number }}, 卡片分类: {{ log.card_category }}, 进出标志: {{ log.in_out_symbol }}, MC ID: {{ log.mc_id }}, 测试时间: {{ log.test_datetime }}, 测试结果: {{ log.test_result }}, 是否测试: {{ log.is_tested }}, 手测试值: {{ log.hand }}, 左脚测试值: {{ log.left_foot }}, 右脚测试值: {{ log.right_foot }}</p>
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

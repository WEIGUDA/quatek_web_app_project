<template>
  <div class="form">
    <div class="form-group">
      <label for="smtp_host">SMTP IP or Domain Name</label>
      <input type="text" class="form-control" id="smtp_host" v-model="config.smtp_host">
    </div>

    <div class="form-group">
      <label for="smtp_port">SMTP Port</label>
      <input type="text" class="form-control" id="smtp_port" v-model="config.smtp_port">
    </div>

    <div class="form-group">
      <label for="smtp_username">SMTP 用户名</label>
      <input type="text" class="form-control" id="smtp_username" v-model="config.smtp_username">
    </div>

    <div class="form-group">
      <label for="smtp_password">SMTP 密码</label>
      <input type="text" class="form-control" id="smtp_password" v-model="config.smtp_password">
    </div>

    <div class="form-group form-check">
      <input type="checkbox" class="form-check-input" id="smtp_use_ssl" v-model="config.smtp_use_ssl">
      <label class="form-check-label" for="smtp_use_ssl">使用SSL</label>
    </div>
    <div class="form-group form-check">
      <input type="checkbox" class="form-check-input" id="smtp_use_tls" v-model="config.smtp_use_tls">
      <label class="form-check-label" for="smtp_use_tls">使用TLS</label>
    </div>
    <hr>

    <div class="form-group">
      <label for="emalis">Email (用于接受报告)</label>
      <input type="text" class="form-control" id="emalis" v-model="config.emails">
      <small id="emailsHelp" class="form-text text-muted">格式: a@example.com,b@example.com</small>
    </div>
    <hr>
    <div class="form-group">
      <label for="work_hours">工作时间</label>
      <input type="text" class="form-control" id="work_hours" v-model="config.work_hours">
      <small id="work_hours_help" class="form-text text-muted">格式: 8:00-18:00</small>
    </div>

    <button type="button" class="btn btn-success btn-quatek" @click.prevent.stop="submit()">确定</button>
  </div>
</template>

<script>
import axios from 'axios';
import lodash from 'lodash';
export default {
  data: function() {
    return {
      config: {
        smtp_host: '',
        smtp_port: '465',
        smtp_use_ssl: true,
        smtp_use_tls: true,
        smtp_username: '',
        smtp_password: '',
        emails: '',
        work_hours: '8:00-18:00',
      },
    };
  },
  methods: {
    submit() {
      console.log(this.config);
      axios
        .post('update-system-config', this.config)
        .then((response) => {
          console.log(response.data);
        })
        .catch((response) => {
          console.log(response);
        });
    },
    get_system_config() {
      axios
        .get('get-system-config')
        .then((response) => {
          console.log(response.data);
          this.config = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },
  },
  created() {
    this.get_system_config();
  },
};
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>

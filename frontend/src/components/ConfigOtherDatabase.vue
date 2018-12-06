<template>
  <div class="form">
    <div class="form-group">
      <label for="db_type">数据库类型</label>
      <select name="db_type" id="db_type" class="form-control" v-model="config.db_type">
        <option value>------------</option>
        <option value="oracle">Oracle</option>
      </select>
    </div>

    <div class="form-group">
      <label for="db_name">数据库名称</label>
      <input type="text" class="form-control" id="db_name" v-model="config.db_name">
    </div>

    <div class="form-group">
      <label for="db_host">数据库地址</label>
      <input type="text" class="form-control" id="db_host" v-model="config.db_host">
    </div>

    <div class="form-group">
      <label for="db_port">数据库端口</label>
      <input type="text" class="form-control" id="db_port" v-model="config.db_port">
    </div>

    <div class="form-group">
      <label for="db_username">数据库用户名</label>
      <input type="text" class="form-control" id="db_username" v-model="config.db_username">
    </div>

    <div class="form-group">
      <label for="db_password">数据库密码</label>
      <input type="text" class="form-control" id="db_password" v-model="config.db_password">
    </div>

    <hr>

    <button type="button" class="btn btn-success btn-quatek" @click.prevent.stop="submit()">确定</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: function() {
    return {
      config: {
        db_type: "",
        db_name: "",
        db_host: "",
        db_port: "",
        db_username: "",
        db_password: ""
      }
    };
  },
  methods: {
    submit() {
      console.log(this.config);
      axios
        .post("/update-other-database-config", this.config)
        .then(response => {
          console.log(response.data);
          alert("保存成功!");
        })
        .catch(response => {
          console.log(response);
          alert("保存失败!");
        });
    },

    get_other_database_config() {
      axios
        .get("/get-other-database-config")
        .then(response => {
          console.log(response.data);
          this.config = response.data;
        })
        .catch(response => {
          console.log(response);
        });
    }
  },
  created() {
    this.get_other_database_config();
  }
};
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>

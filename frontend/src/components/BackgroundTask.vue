<template>
  <div class="form">

    <button type="button" class="btn btn-success btn-quatek" :disabled="is_button_disabled" @click.prevent.stop="sync_cards()">同步卡片信息</button>
    <br>
    <br>
    <br>
    <button type="button" class="btn btn-success btn-quatek" :disabled="is_button_disabled" @click.prevent.stop="delete_all_cards()">删除闸机上卡片信息</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data: function() {
    return {
      is_button_disabled: false,
    };
  },
  methods: {
    sync_cards() {
      this.is_button_disabled = true;
      axios
        .post('sync-cards')
        .then((response) => {
          console.log(response.data);
        })
        .catch((response) => {
          console.log(response);
        });
      setTimeout(() => {
        this.is_button_disabled = false;
      }, 30000);
    },
    delete_all_cards() {
      this.is_button_disabled = true;
      axios
        .post('delete-all-cards')
        .then((response) => {
          console.log(response.data);
        })
        .catch((response) => {
          console.log(response);
        });
      setTimeout(() => {
        this.is_button_disabled = false;
      }, 30000);
    },
  },
  created() {},
};
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>

<template>
  <div class="container">
    <table class="table table-striped">
      <tr>
        <td>#</td>
        <td>实例</td>
        <td>错误</td>
      </tr>

      <tr v-for="(error, index) in getLastFailedUpload" v-bind:key="index">
        <td>{{ index + 1}}</td>
        <td>{{error[0]}}</td>
        <td>{{error[1]}}</td>
      </tr>
    </table>
  </div>
</template>
<script>
import { mapGetters, mapMutations } from "vuex";

export default {
  computed: {
    ...mapGetters(["getLastFailedUpload"]),
    myOwn() {
      return null;
    }
  },
  methods: {
    ...mapMutations(["setLastFailedUpload"]),
    myOwnMethod() {
      return null;
    }
  }
};
</script>
<style scoped>
</style>

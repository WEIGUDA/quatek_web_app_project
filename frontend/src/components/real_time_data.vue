<template>
  <div>
    <p v-for="log in get_logs" :key="log.log_id">{{log}}</p>
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

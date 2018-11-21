<template>
  <div class="container">
    <div class="card card-container login-card">
      <form class="form-signin">
        <input type="text" id="inputEmail" class="form-control" placeholder="用户名" autofocus v-model="username">
        <br>
        <input type="password" id="inputPassword" class="form-control" placeholder="密码" v-model="password">
        <br>
        <button class="btn btn-lg btn-success btn-block btn-signin btn-quatek" @click.stop.prevent="login({username: username, password: password})" type="submit">登入</button>
      </form><!-- /form -->

    </div><!-- /card-container -->
  </div><!-- /container -->
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'login',
  data: function() {
    return {
      username: '',
      password: '',
    };
  },
  props: {},
  methods: {
    ...mapActions(['login']),
  },
  components: {},
};
</script>

<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
.login-card {
  margin: 100px 0 0 0;
  border: none;
}
.btn-quatek {
  background-color: #059c66;
}
/*  Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
}

/*  Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
}

/*  Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
  .login-card {
    margin: 100px 0 200px 0;
  }
}

/*  Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
}
</style>

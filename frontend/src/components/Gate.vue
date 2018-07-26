<template>
  <div class="col-md-3 text-center gate-box">
    <p class="text-right gate-indicator-row">
      <span class="badge gate-badge">
        <font-awesome-icon icon="circle" />
      </span>
    </p>

    <img src="@/assets/gate.png" class="img-fluid gate-img" alt="Gate image">
    <div class="w-100"></div>
    <div class="btn-group btn-group-sm text-center" role="group" aria-label="On OFF Buttons">
      <button type="button" class="btn gate-btn-on-off" :class="{ 'btn-dark': isOn }" @click.prevent="toggleIsOn()">ON</button>
      <button type="button" class="btn gate-btn-on-off" :class="{ 'btn-dark': !isOn }" @click.prevent="toggleIsOn()">OFF</button>
    </div>
    <div class="w-100">
      <table class="gate-table">
        <tr>
          <td rowspan="2" class="text-center align-middle gate-icon">
            <font-awesome-icon icon="shoe-prints" :transform="{ rotate: 270 }" size="2x" />
          </td>

          <td class="gate-max-min-left-td">max</td>
          <td class="gate-value-left-td">{{gate.hand_max}}</td>
          <td></td>
          <td class="gate-value-right-td">{{gate.foot_max}}</td>
          <td class="gate-max-min-right-td">max</td>

          <td rowspan="2" class="text-center align-middle gate-icon">
            <font-awesome-icon icon="hand-paper" size="2x" />
          </td>
        </tr>
        <tr>
          <td class="gate-max-min-left-td">min</td>
          <td class="gate-value-left-td">{{gate.hand_min}}</td>
          <td></td>
          <td class="gate-value-right-td">{{gate.foot_min}}</td>
          <td class="gate-max-min-right-td">min</td>
        </tr>
      </table>
    </div>

  </div>
</template>
<script>
export default {
  name: 'Gate',
  data() {
    return {
      isOn: this.gate.is_on,
    };
  },
  props: {
    gate: null,
  },
  methods: {
    toggleIsOn() {
      this.isOn = !this.isOn;
    },
  },
  components: {},
  created() {},
};
</script>

<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.gate-box {
  margin-bottom: 40px;
}
.gate-indicator-row {
  margin-bottom: 0;
}
.gate-badge {
  color: #059c66;
}
.gate-img {
  width: 70%;
  margin-bottom: 10px;
}
.gate-btn-on-off {
  width: 80px;
}
.gate-table {
  margin: 10px auto 0 auto;
  width: 90%;
  padding: 0;
  color: #343a40;
}
.gate-icon {
  color: #898989;
}
.gate-value-left-td {
  border: 1px solid #898989;
  color: #898989;
}
.gate-value-right-td {
  border: 1px solid #898989;
  color: #898989;
}
.gate-max-min-left-td {
  color: #898989;
}
.gate-max-min-right-td {
  color: #898989;
}

@media (min-width: 576px) {
}

/*  Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
  .gate-btn-on-off {
    width: 40px;
  }
}

/*  Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
  .gate-btn-on-off {
    width: 70px;
  }
}

/*  Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
  .gate-value-left-td {
    padding: 0 6px;
  }
  .gate-value-right-td {
    padding: 0 6px;
  }
  .gate-max-min-left-td {
    padding: 0 5px;
  }
  .gate-max-min-right-td {
    padding: 0 5px;
  }
}
</style>



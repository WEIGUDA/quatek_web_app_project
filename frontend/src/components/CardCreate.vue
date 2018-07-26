<template>
  <div class="container">
    <form class="card-create-form">
      <div class="form-group row">
        <label for="cardNumber" class="col-sm-2 col-form-label">卡号 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="cardNumber" v-model="card.card_number">

        </div>

      </div>

      <div class="form-group row">
        <label for="card_category" class="col-sm-2 col-form-label">卡类别 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="card_category" v-model="card.card_category">
          <small class="form-text text-muted">0: 手脚同测, 1: 只测手, 2: 只测脚, 4: VIP</small>
        </div>
      </div>

      <div class="form-group row">
        <label for="name" class="col-sm-2 col-form-label">姓名 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="name" v-model="card.name">
        </div>
      </div>

      <div class="form-group row">
        <label for="job_number" class="col-sm-2 col-form-label">工号 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="job_number" v-model="card.job_number">
        </div>
      </div>

      <div class="form-group row">
        <label for="department" class="col-sm-2 col-form-label">部门 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="department" v-model="card.department">
        </div>
      </div>

      <div class="form-group row">
        <label for="gender" class="col-sm-2 col-form-label">性别 *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="gender" v-model="card.gender">
          <small class="form-text text-muted">0: 女, 1: 男</small>
        </div>
      </div>

      <div class="form-group row">
        <label for="note" class="col-sm-2 col-form-label">其他</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="note" v-model="card.note">
        </div>
      </div>

      <div class="form-group row">
        <label for="belong_to_mc" class="col-sm-2 col-form-label">对应闸机&权限</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="belong_to_mc" v-model="card.belong_to_mc">
          <small class="form-text text-muted">format: "gate_1:0|gate_2:1|gate_3:3"; 其中0:可进可出, 1:禁止进入/可出, 2:禁止出去/可进, 3:禁止进出; "all"填代表对应所有闸机</small>
        </div>
      </div>

      <div class="form-group row text-center">
        <div class="col-sm-12">
          <button type="submit" class="btn btn-success btn-block submit-btn" @click.prevent="submit()" :disabled="submit_is_disabled"> 保存 </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: '',
  data: function() {
    return {
      card: {
        id: '',
        card_number: '',
        card_category: '',
        name: '',
        job_number: '',
        department: '',
        gender: '',
        note: '',
        belong_to_mc: '',
      },
      submit_is_disabled: false,
    };
  },
  methods: {
    submit() {
      this.submit_is_disabled = true;
      console.log(this.card);
      if (
        this.card.card_number &&
        this.card.card_category &&
        this.card.name &&
        this.card.job_number &&
        this.card.department &&
        this.card.gender
      ) {
        if (this.card.id) {
          axios
            .patch('cards/create', this.card)
            .then((response) => {
              console.log(response);
              alert('保存成功!');
              this.$router.push({ name: 'Cards' });
            })
            .catch((response) => {
              console.log(response);
              alert('保存失败!');
              this.submit_is_disabled = false;
            });
        } else {
          axios
            .post('cards/create', this.card)
            .then((response) => {
              console.log(response);
              alert('保存成功!');
              this.$router.push({ name: 'Cards' });
            })
            .catch((response) => {
              console.log(response);
              alert('保存失败!');
              this.submit_is_disabled = false;
            });
        }
      } else {
        alert('带*的信息不能为空!');
      }
    },
  },
  created() {
    if (this.$route.params.card_id) {
      this.card.id = this.$route.params.card_id;
      axios
        .get(`cards?q=${this.card.id}`)
        .then((response) => {
          console.log(response);
          this.card.card_number = response.data[0].card_number;
          this.card.card_category = response.data[0].card_category;
          this.card.name = response.data[0].name;
          this.card.job_number = response.data[0].job_number;
          this.card.department = response.data[0].department;
          this.card.gender = response.data[0].gender;
          this.card.note = response.data[0].note;
          this.card.belong_to_mc = response.data[0].belong_to_mc;
          this.card.number_in_mc = response.data[0].number_in_mc;
          console.log(this.card);
        })
        .catch((response) => {
          console.log(response);
        });
    }
  },
};
</script>


<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.submit-btn {
  color: #ffffff;
  background-color: #059c66;
}
.vdatetime-popup__header {
  background-color: #059c66;
}

@media (min-width: 576px) {
}

/*  Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
}

/*  Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
}

/*  Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
  .card-create-form {
    margin-top: 60px;
  }
  .submit-btn {
    margin-top: 30px;
  }
}
</style>
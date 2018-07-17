<template>
    <div class="container">
        <form class="card-create-form">
            <div class="form-group row">
                <label for="name" class="col-sm-2 col-form-label">姓名 *</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="name" v-model="ooo.key1">
                </div>
            </div>
            {{ooo.key1}}

            <div class="form-group row">
                <label for="cardNumber" class="col-sm-2 col-form-label">卡号 *</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="cardNumber">
                </div>
            </div>

            <div class="form-group row">
                <label for="phone" class="col-sm-2 col-form-label">电话</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="phone">
                </div>
            </div>

            <div class="form-group row">
                <label for="position" class="col-sm-2 col-form-label">职位</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="position">
                </div>
            </div>

            <div class="form-group row">
                <label for="enterDate" class="col-sm-2 col-form-label">入职时间</label>
                <div class="col-sm-10">
                    <datetime v-model="date1" type="date" input-class="form-control" format="yyyy-MM-dd" :phrases="{ok: '确定', cancel: '取消'}" :minute-step="10"></datetime>
                </div>
            </div>

            <div class="form-group row">
                <label for="jobNumber" class="col-sm-2 col-form-label">工号 *</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="jobNumber" />
                </div>
            </div>

            <fieldset class="form-group">
                <div class="row">
                    <legend class="col-form-label col-sm-2 pt-0">性别</legend>
                    <div class="col-sm-10">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="gridRadios" id="gridRadios1" value="option1" checked>
                            <label class="form-check-label" for="gridRadios1">
                                男
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="gridRadios" id="gridRadios2" value="option2">
                            <label class="form-check-label" for="gridRadios2">
                                女
                            </label>
                        </div>
                    </div>
                </div>
            </fieldset>

            <div class="form-group row">
                <label for="cardCategory" class="col-sm-2 col-form-label">卡类型</label>
                <div class="col-sm-10">
                    <select class="form-control" id="cardCategory">
                        <option>1</option>
                        <option>2</option>
                        <option>3</option>
                        <option>4</option>
                        <option>5</option>
                    </select>
                </div>
            </div>

            <div class="form-group row">
                <label for="birthday" class="col-sm-2 col-form-label">出生</label>
                <div class="col-sm-10">
                    <datetime v-model="date1" type="date" input-class="form-control" format="yyyy-MM-dd" :phrases="{ok: '确定', cancel: '取消'}" :minute-step="10"></datetime>

                </div>
            </div>

            <div class="form-group row">
                <label for="department" class="col-sm-2 col-form-label">部门</label>
                <div class="col-sm-10">
                    <select class="form-control" id="department">
                        <option>1</option>
                        <option>2</option>
                        <option>3</option>
                        <option>4</option>
                        <option>5</option>
                    </select>
                </div>
            </div>

            <div class="form-group row text-center">
                <div class="col-sm-12">
                    <button type="submit" class="btn btn-success btn-block submit-btn" @click.prevent="submitOoo()"> 保存 </button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
  name: '',
  data: function() {
      return {
          date1: this.$moment().format('YYYY-MM-DDTHH:mm:ss'),
          ooo: {key1: '', key2: ''}
          
      };
  },
  props: {
 
  },
  components: {
    },
    methods: {
     submitOoo() {
         console.log(this.ooo);
     }   
    }
}
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
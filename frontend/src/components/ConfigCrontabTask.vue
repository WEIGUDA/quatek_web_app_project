<template>
  <div>
    <form class="form-inline">

      <label class="sr-only" for="task">任务</label>
      <select name="task" id="task" class="custom-select  mb-2 mr-sm-2" v-model="crontab_task.task">
        <option value="">------请选择任务------</option>
        <option value="app.mod_task.tasks.send_email_of_logs:">任务: 发送所有班别报告</option>
        <option value="app.mod_task.tasks.get_logs_from_mc_task">任务: 从闸机获取Logs</option>
        <option value="app.mod_task.tasks.save_to_other_database">任务: 保存到其他数据库</option>
        <option v-for="card_class in card_classes" :value="'app.mod_task.tasks.send_email_of_logs:'+card_class.name" :key="card_class.name">任务: 发送{{card_class.name}}班别报告</option>

      </select>

      <label class="sr-only" for="minute">分</label>
      <div class="input-group mb-2 mr-sm-2">
        <input type="text" class="form-control" id="minute" v-model="crontab_task.minute" placeholder="0 - 59">
        <div class="input-group-append">
          <div class="input-group-text">分</div>
        </div>
      </div>

      <label class="sr-only" for="hour">时</label>
      <div class="input-group mb-2 mr-sm-2">
        <input type="text" class="form-control" id="hour" v-model="crontab_task.hour" placeholder="0 - 23">
        <div class="input-group-append">
          <div class="input-group-text">时</div>
        </div>
      </div>

      <label class="sr-only" for="day_of_month">日</label>
      <div class="input-group mb-2 mr-sm-2">
        <input type="text" class="form-control" id="day_of_month" v-model="crontab_task.day_of_month" placeholder="1 - 31">
        <div class="input-group-append">
          <div class="input-group-text">日</div>
        </div>
      </div>

      <label class="sr-only" for="month_of_year">周</label>
      <select name="task" id="month_of_year" class="custom-select  mb-2 mr-sm-2" v-model="crontab_task.month_of_year">
        <option value="*">所有月</option>
        <option value="1">一月</option>
        <option value="2">二月</option>
        <option value="3">三月</option>
        <option value="4">四月</option>
        <option value="5">五月</option>
        <option value="6">六月</option>
        <option value="7">七月</option>
        <option value="8">八月</option>
        <option value="9">九月</option>
        <option value="10">十月</option>
        <option value="11">十一月</option>
        <option value="12">十二月</option>
      </select>

      <label class="sr-only" for="day_of_week">月</label>
      <select name="task" id="day_of_week" class="custom-select  mb-2 mr-sm-2" v-model="crontab_task.day_of_week">
        <option value="*">周日到周一</option>
        <option value="0">周日</option>
        <option value="1">周一</option>
        <option value="2">周二</option>
        <option value="3">周三</option>
        <option value="4">周四</option>
        <option value="5">周五</option>
        <option value="6">周六</option>
      </select>

      <button type="submit" class="btn btn-success mb-2 btn_quatek" @click.prevent.stop="submit()">添加</button>

    </form>
    <small id="passwordHelpBlock" class="form-text text-muted">
      了解更多:
      <a href="https://zh.wikipedia.org/wiki/Cron" target="_blank">crontab wikipedia</a>
      <span> &#160;</span>
      大陆用户请使用:
      <a href="https://baike.baidu.com/item/crontab/8819388" target="_blank">crontab 百度百科</a>
    </small>
    <br>
    <div>
      <div class="row">
        <table class="table table-striped table-responsive-md">
          <thead>
            <tr>
              <th scope="col">任务</th>
              <th scope="col">运行日期(分|时|日|月|周)</th>
              <th scope="col">删除</th>

            </tr>
          </thead>

          <tbody v-if="!tasks.length">
            <tr>
              <td colspan="3" class="text-center">没有找到任务</td>
            </tr>

          </tbody>

          <tbody v-if="tasks.length">
            <tr v-for="task in computed_tasks" :key="task._id.$oid">
              <td>{{task.task}} <span v-if="task.kwargs.card_class_time">: {{task.kwargs.card_class_time}} 班别</span></td>
              <td>{{task.crontab.minute}} | {{task.crontab.hour}} | {{task.crontab.day_of_month}} | {{task.crontab.month_of_year}} | {{task.crontab.day_of_week}}</td>
              <td>
                <button type=" button" class="btn btn-secondary btn-quatek btn-sm" @click="delete_task(task._id.$oid)">
                  <font-awesome-icon icon="trash-alt" />
                </button>
              </td>
            </tr>
          </tbody>

        </table>
      </div>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import lodash from 'lodash';
export default {
  data: function() {
    return {
      tasks: [],
      crontab_task: {
        task: '',
        minute: '*',
        hour: '*',
        day_of_month: '*',
        month_of_year: '*',
        day_of_week: '*',
      },
      card_classes: [],
    };
  },
  computed: {
    computed_tasks() {
      let computed_tasks = lodash.cloneDeep(this.tasks);
      for (let task of computed_tasks) {
        if (task.task.indexOf('get_logs_from_mc_task') >= 0) {
          task.task = '从闸机获取Logs';
        } else if (task.task.indexOf('send_email_of_logs') >= 0) {
          task.task = '发送报告';
        } else if (task.task.indexOf('save_to_other_database') >= 0) {
          task.task = '保存到其他数据库';
        }
      }
      return computed_tasks;
    },
  },
  methods: {
    submit() {
      if (this.crontab_task.task.length == 0) {
        return;
      }
      if (
        !(
          this.crontab_task.minute === '*' ||
          (Number(this.crontab_task.minute) <= 59 && Number(this.crontab_task.minute) >= 0)
        )
      ) {
        alert('分 设置错误!');
        return;
      }
      if (
        !(
          this.crontab_task.hour === '*' ||
          (Number(this.crontab_task.hour) <= 23 && Number(this.crontab_task.hour) >= 0)
        )
      ) {
        alert('时 设置错误!');
        return;
      }
      if (
        !(
          this.crontab_task.day_of_month === '*' ||
          (Number(this.crontab_task.day_of_month) <= 31 && Number(this.crontab_task.day_of_month) >= 1)
        )
      ) {
        alert('日 设置错误!');
        return;
      }
      axios
        .get(`does-task-exist?q=${this.crontab_task.task}`)
        .then((response) => {
          console.log(response.data);
          if (response.data.does_task_exist === false) {
            axios
              .post('task-crontab-add-one', {
                task: this.crontab_task.task,
                minute: this.crontab_task.minute,
                hour: this.crontab_task.hour,
                day_of_month: this.crontab_task.day_of_month,
                month_of_year: this.crontab_task.month_of_year,
                day_of_week: this.crontab_task.day_of_week,
              })
              .then((response) => {
                console.log(response.data);
                this.get_tasks();
              })
              .catch((response) => {
                console.log(response);
              });
          } else {
            alert('当前任务已经存在, 请勿重复添加!');
          }
        })
        .catch((response) => {
          console.log(response);
        });

      console.log(this.crontab_task);
    },
    delete_task(task_id) {
      axios
        .post('task-delete', { task_id: task_id })
        .then((response) => {
          console.log(response.data);
          this.get_tasks();
        })
        .catch((response) => {
          console.log(response);
        });
    },

    get_tasks() {
      axios
        .get('task-crontab')
        .then((response) => {
          console.log(response);
          this.tasks = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },

    get_class_times() {
      axios
        .get('get-class-times')
        .then((response) => {
          console.log(response);
          this.card_classes = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },
  },

  created() {
    this.get_tasks();
    this.get_class_times();
  },
};
</script>

<style scoped>
.btn_quatek {
  background-color: #059c66;
}
</style>



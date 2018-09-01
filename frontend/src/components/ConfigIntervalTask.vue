<template>
  <div>
    <form class="form-inline">

      <label class="sr-only" for="task">任务</label>
      <select name="task" id="task" class="custom-select  mb-2 mr-sm-2" v-model="interval_task.task">
        <option value="">------请选择任务------</option>
        <option value="app.mod_task.tasks.send_email_of_logs">任务: 发送报告</option>
        <option value="app.mod_task.tasks.get_logs_from_mc_task">任务: 从闸机获取Logs</option>
        <option value="app.mod_task.tasks.save_to_other_database">任务: 保存到其他数据库</option>
      </select>

      <label class="sr-only" for="every">每{{interval_task.every}}秒运行一次</label>
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">每</div>
        </div>
        <input type="text" class="form-control" id="every" v-model="interval_task.every" placeholder="每?秒运行一次">
        <div class="input-group-append">
          <div class="input-group-text">秒运行一次</div>
        </div>
      </div>

      <button type="submit" class="btn btn-success mb-2 btn_quatek" @click.prevent.stop="submit()">添加</button>
    </form>
    <br>
    <div>
      <div class="row">
        <table class="table table-striped table-responsive-md">
          <thead>
            <tr>
              <th scope="col">任务</th>
              <th scope="col">运行间隔</th>
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
              <td>{{task.task}}</td>
              <td>{{task.interval.every}}</td>
              <td>
                <button type="button" class="btn btn-secondary btn-quatek btn-sm" @click="delete_task(task._id.$oid)">
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
      interval_task: {
        task: '',
        every: '60',
      },
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
      if (this.interval_task.task.length == 0) {
        return;
      }
      axios
        .get(`does-task-exist?q=${this.interval_task.task}`)
        .then((response) => {
          console.log(response.data);
          if (response.data.does_task_exist === false) {
            axios
              .post('task-interval-add-one', { every: this.interval_task.every, task: this.interval_task.task })
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

      console.log(this.interval_task);
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
        .get('task-interval')
        .then((response) => {
          console.log(response);
          this.tasks = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },
  },

  created() {
    this.get_tasks();
  },
};
</script>

<style scoped>
.btn_quatek {
  background-color: #059c66;
}
</style>



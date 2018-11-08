<template>
  <div class="container">
    <div class="row search-row">
      <div class="input-group">
        <input type="text" class="form-control" aria-label="Search string" aria-describedby="basic-addon2" v-model.trim="query_string" placeholder="可搜索卡号, 卡类别, 姓名, 工号和部门">
        <div class="input-group-append">
          <button class="btn btn-outline-success btn-outline-quatek" type="button" @click="search()">
            <font-awesome-icon icon="search" /> Search</button>
        </div>
      </div>
    </div>
    <div class="row btn-row">
      <p class="w-100 text-right">
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="上传" @click="upload_show()">
          <font-awesome-icon icon="upload" />
        </button>
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="下载" @click="download_excel()">
          <font-awesome-icon icon="download" />
        </button>
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="添加卡片" @click="cardAdd()">
          <font-awesome-icon icon="user-plus" />
        </button>
      </p>
    </div>
    <div class="row" v-if="!cards.length">
      <p class="w-100 text-center no-result">没有搜索到结果</p>
    </div>
    <div class="row" v-if="cards.length">
      <table class="table table-striped table-responsive-md">
        <thead>
          <tr>
            <th scope="col">姓名</th>
            <th scope="col">工号</th>
            <th scope="col">卡号</th>
            <th scope="col">卡类型</th>
            <th scope="col">部门</th>
            <th scope="col">班别</th>
            <th scope="col">修改</th>
            <th scope="col">删除</th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="card in computed_cards" :key="card._id.$oid">
            <td>{{card.name}}</td>
            <td>{{card.job_number}}</td>
            <td>{{card.card_number}}</td>
            <td>{{card.card_category}}</td>
            <td>{{card.department}}</td>
            <td>{{card.class_time}}</td>
            <td>
              <button type="button" class="btn btn-secondary btn-quatek btn-sm" @click="edit_card(card._id.$oid)">
                <font-awesome-icon icon="pencil-alt" />
              </button>
            </td>
            <td>
              <button type="button" class="btn btn-secondary btn-quatek btn-sm" @click="delete_cards([card._id.$oid,])">
                <font-awesome-icon icon="trash-alt" />
              </button>
            </td>
          </tr>
        </tbody>

      </table>
    </div>
    <nav aria-label="Page navigation" v-if="cards.length">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{disabled: currentPage<=1}">
          <a class="page-link" href="#" aria-label="Previous" @click="prevPage()">
            <span aria-hidden="true">&laquo;</span>
            <span class="sr-only">上一页</span>
          </a>

        </li>
        <li class="page-item disabled">
          <a class="page-link">第 {{currentPage}} 页</a>
        </li>

        <li class="page-item">
          <a class="page-link" href="#" aria-label="Next" @click="nextPage()">
            <span aria-hidden="true">&raquo;</span>
            <span class="sr-only">下一页</span>
          </a>
        </li>

      </ul>
    </nav>
    <b-modal v-model="show_modal" title="上传卡片信息" ok-only ok-title="上传" :lazy="true" @ok="upload2()" ok-variant="success">
      <b-container fluid>
        <b-row>
          <a class="template_download" href="" @click.prevent="download_cards_upload_template2()">卡片上传模版.xlsx</a>
        </b-row>
        <br>
        <b-row>
          <input type="file" name="excel_file" id="excel_file" ref="excel_file">
        </b-row>

      </b-container>
    </b-modal>

    <b-modal v-model="show_modal2" title="上传卡片信息" ok-only ok-title="查看详情" :lazy="true" @ok="routeToFailedUploadPage()" ok-variant="success">
      <b-container fluid>
        <b-row>
          {{this.last_upload_result.result}} 张卡片上传成功
        </b-row>
        <br>
        <b-row>
          {{this.last_upload_result.failed_numbers}} 张失败
        </b-row>

      </b-container>
    </b-modal>
  </div>
</template>

<script>
import lodash from 'lodash';
import axios from 'axios';
import fileDownload from 'js-file-download';
export default {
  name: 'Cards',
  data() {
    return {
      currentPage: 1,
      cards: [],
      query_string: '',
      show_modal: false,
      cards_file: '',
      excel_file: '',
      show_modal2: false,
      last_upload_result: {},
    };
  },
  computed: {
    computed_cards: function() {
      let computed_cards = lodash.cloneDeep(this.cards);
      for (let card of computed_cards) {
        if (card.card_category === '0') {
          card.card_category = 'vip';
        } else if (card.card_category === '1') {
          card.card_category = '只测手';
        } else if (card.card_category === '2') {
          card.card_category = '只测脚';
        } else if (card.card_category === '3') {
          card.card_category = '手脚都测';
        }
      }
      return computed_cards;
    },
  },
  methods: {
    cardAdd() {
      this.$router.push({ name: 'CardCreate' });
    },
    search() {
      console.log(this.query_string);
      this.currentPage = 1;

      axios
        .get(`cards?q=${this.query_string}`)
        .then((response) => {
          console.log(response);
          this.cards = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },

    edit_card(card_id) {
      this.$router.push({ name: 'CardEdit', params: { card_id: card_id } });
    },

    upload_show() {
      this.show_modal = true;
    },

    upload2() {
      let formData = new FormData();
      let excel_file = this.$refs.excel_file.files[0];
      formData.append('excel_file', excel_file);
      console.log(formData);
      axios
        .post('upload_cards_excel', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          console.log(response);
          this.last_upload_result = response.data;
          this.$store.commit('setLastFailedUpload', response.data.failed);
          this.show_modal2 = true;
        })
        .catch((response) => {
          console.log(response);
        });
    },

    routeToFailedUploadPage() {
      this.$router.push({ name: 'LastFailedUpload' });
    },

    download_cards_upload_template2() {
      axios
        .get('download_cards_upload_template', {
          responseType: 'blob',
        })
        .then((response) => {
          console.log(response);
          fileDownload(
            response.data,
            '卡片上传模版.xlsx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          );
        })
        .catch((response) => {
          console.log(response);
        });
    },

    delete_cards(cards_array) {
      let delete_confirmed = prompt('请输入 YES 确认删除!');
      if (delete_confirmed === 'YES') {
        let delete_array = JSON.stringify(cards_array);
        console.log(delete_array);
        axios
          .delete(`cards?delete_array=${delete_array}`)
          .then((response) => {
            console.log(response);
            alert('删除成功!');
            this.get_cards();
          })
          .catch((response) => {
            console.log(response);
            alert('无法删除!');
          });
      } else if (delete_confirmed === null) {
        console.log('canceled');
      } else {
        alert('输入错误');
      }
    },

    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      axios
        .get(`cards?offset=${offset}&q=${this.query_string}`)
        .then((response) => {
          console.log(response);
          this.cards = response.data;
          this.currentPage--;
        })
        .catch((response) => {
          console.log(response);
        });
    },
    nextPage() {
      let offset = this.currentPage * 50;
      axios
        .get(`cards?offset=${offset}&q=${this.query_string}`)
        .then((response) => {
          if (response.data.length !== 0) {
            console.log(response);
            this.cards = response.data;
            this.currentPage++;
          } else {
            alert('已经到达最后一页!');
          }
        })
        .catch((response) => {
          console.log(response);
        });
    },
    download_csv() {
      try {
        let title = 'cards_page_' + this.currentPage;
        let card_array = [];
        let csv_header =
          'id,card_number,card_category,name,job_number,department,gender,note,belong_to_mc,number_in_mc,created_time\n';
        let csv = [];

        for (let card of this.computed_cards) {
          card_array.push(
            [
              card._id.$oid,
              card.card_number,
              card.card_category,
              card.name,
              card.job_number,
              card.department,
              card.gender,
              card.note,
              card.belong_to_mc,
              card.number_in_mc,
              this.$moment(card.created_time.$date).format(),
            ].join(','),
          );
        }
        csv = card_array.join('\n');

        let uri = 'data:text/csv;charset=utf-8,' + csv_header + encodeURI(csv);

        let link = document.createElement('a');

        link.id = 'csv-download-id';
        link.href = uri;

        document.body.appendChild(link);

        document.getElementById(link.id).style.visibility = 'hidden';
        document.getElementById(link.id).download = title + '.csv';

        document.body.appendChild(link);
        document.getElementById(link.id).click();

        setTimeout(function() {
          document.body.removeChild(link);
        });
        return true;
      } catch (err) {
        return false;
      }
    },

    download_excel() {
      axios
        .get('download-cards', {
          responseType: 'blob',
        })
        .then((response) => {
          console.log(response);
          fileDownload(response.data, '卡片.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        })
        .catch((response) => {
          console.log(response);
        });
    },

    get_cards() {
      axios
        .get('cards')
        .then((response) => {
          console.log(response);
          this.cards = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },
  },

  created() {
    this.get_cards();
  },
};
</script>


<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.search-row {
  margin: 0 0 20px 0;
}
.btn-outline-quatek {
  color: #059c66;
  border-color: #059c66;
}

.btn-row-btn {
  margin: 0 5px;
  background-color: #868686;
}
.btn-quatek {
  background-color: #868686;
}

.page-link {
  color: #059c66;
}
.template_download {
  color: #059c66;
}
.no-result {
  height: 300px;
  color: #868686;
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
  .search-row {
    margin: 0 -15px 20px -15px;
  }
  .no-result {
    height: 400px;
  }
}
</style>


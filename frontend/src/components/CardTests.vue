<template>
  <div class="container">
    <div class="form-row search-row">
      <div class="input-group">

        <datetime v-model="datetime_from" type="datetime" input-class="form-control" format="yyyy-MM-dd HH:mm" :phrases="{ok: '确定', cancel: '取消'}" :minute-step="10"></datetime>

        <label class="col-sm-1 text-center search-space"> 至 </label>

        <datetime v-model="datetime_to" type="datetime" input-class="form-control" format="yyyy-MM-dd HH:mm" :phrases="{ok: '确定', cancel: '取消'}" :minute-step="10"></datetime>

      </div>
      <div class="w-100"><br></div>
      <div class="input-group">
        <input type="text" class="form-control" aria-label="Search string" aria-describedby="basic-addon2" v-model.trim="query_string" placeholder="可搜索闸机名称或卡号">
        <div class="input-group-append">
          <button class="btn btn-outline-success btn-outline-quatek" type="button" @click="search()">
            <font-awesome-icon icon="search" /> Search</button>
        </div>
      </div>
    </div>
    <div class="row btn-row">
      <p class="w-100 text-right">
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="下载" @click="download_csv()">
          <!-- <font-awesome-icon icon="envelope" /> -->
          <font-awesome-icon icon="download" />
        </button>

      </p>
    </div>
    <div class="row" v-if="!cardtests.length">
      <p class="w-100 text-center no-result">没有搜索到结果</p>
    </div>

    <div class="row" v-if="cardtests.length">
      <table class="table table-striped table-responsive-md">
        <thead>
          <tr>
            <th scope="col">姓名</th>
            <th scope="col">工号</th>
            <th scope="col">卡片类型</th>
            <th scope="col">进出标志</th>
            <th scope="col">闸机名</th>
            <th scope="col">测试时间</th>
            <th scope="col">是否通过</th>
            <th scope="col">是否测试</th>
            <th scope="col">手腕检测值</th>
            <th scope="col">左脚检测值</th>
            <th scope="col">右脚检测值</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cardtest in computed_cardtests" :key="cardtest._id.$oid">
            <td>{{cardtest.name}}</td>
            <td>{{cardtest.job_number}}</td>
            <td>{{cardtest.card_category}}</td>
            <td>{{cardtest.in_out_symbol}}</td>
            <td>{{cardtest.mc_id}}</td>
            <td>{{cardtest.test_datetime.$date | moment('YYYY-MM-DD HH:mm')}}</td>
            <td>{{cardtest.test_result}}</td>
            <td>{{cardtest.is_tested}}</td>
            <td>{{cardtest.hand}}</td>
            <td>{{cardtest.left_foot}}</td>
            <td>{{cardtest.right_foot}}</td>

          </tr>
        </tbody>

      </table>
    </div>
    <nav aria-label="Page navigation" v-if="this.cardtests.length>0">
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
  </div>
</template>

<script>
var lodash = require('lodash');
import axios from 'axios';
export default {
  name: '',
  data() {
    return {
      currentPage: 1,
      cardtests: [],
      query_string: '',
      datetime_from: this.$moment()
        .subtract(24, 'hours')
        .second(0)
        .millisecond(0)
        .format('YYYY-MM-DDTHH:mm'),
      datetime_to: this.$moment()
        .second(0)
        .millisecond(0)
        .format('YYYY-MM-DDTHH:mm'),
      cards: [],
    };
  },
  computed: {
    computed_cardtests: function() {
      let computed_cardtests = lodash.cloneDeep(this.cardtests);
      for (let cardtest of computed_cardtests) {
        let card = this.cards.filter((obj) => obj.card_number === cardtest.card_number);
        if (card.length > 0) {
          cardtest.name = card[0].name;
          cardtest.job_number = card[0].job_number;
        } else {
          cardtest.name = '未找到姓名';
          cardtest.job_number = '未找到工号';
        }
        if (cardtest.test_result === '0') {
          cardtest.test_result = '否';
        } else {
          cardtest.test_result = '是';
        }
      }
      console.log(computed_cardtests);
      return computed_cardtests;
    },
  },
  methods: {
    search() {
      console.log(this.query_string);
      console.log(this.datetime_from);
      console.log(this.datetime_to);

      axios
        .get(`cardtests?q=${this.query_string}&datetime_from=${this.datetime_from}&datetime_to=${this.datetime_to}`)
        .then((response) => {
          console.log(response.data);
          this.cardtests = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },

    download_csv() {
      if (this.cardtests.length > 0) {
        try {
          let title = 'cardtests_page_' + this.currentPage;
          let cardtest_array = [];
          let csv_header =
            'id,card_number,name,job_number,card_category,in_out_symbol,gate_name,test_time,test_result,is_tested,hand_value,left_foot_value,right_foot_value\n';
          let csv = [];

          for (let cardtest of this.computed_cardtests) {
            cardtest_array.push(
              [
                cardtest._id.$oid,
                cardtest.card_number,
                cardtest.name,
                cardtest.job_number,
                cardtest.card_category,
                cardtest.in_out_symbol,
                cardtest.mc_id,
                this.$moment(cardtest.test_datetime.$date).format(),
                cardtest.test_result,
                cardtest.is_tested,
                cardtest.hand,
                cardtest.left_foot,
                cardtest.right_foot,
              ].join(','),
            );
          }
          csv = cardtest_array.join('\n');

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
      } else {
        alert('没有数据可供下载!');
      }
    },

    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      axios
        .get(
          `cardtests?offset=${offset}&q=${this.query_string}&datetime_from=${this.datetime_from}&datetime_to=${
            this.datetime_to
          }`,
        )
        .then((response) => {
          console.log(response.data);
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
        .get(
          `cardtests?offset=${offset}&q=${this.query_string}&datetime_from=${this.datetime_from}&datetime_to=${
            this.datetime_to
          }`,
        )
        .then((response) => {
          if (response.body.length !== 0) {
            console.log(response.data);
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
  },

  created() {
    axios
      .get('cards?offset=0&limit=10000')
      .then((response) => {
        console.log(response);
        this.cards = response.data;
      })
      .catch((response) => {
        console.log(response);
      });
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
.search-space {
  padding-top: 5px;
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
.vdatetime {
  width: 100%;
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
  .vdatetime {
    width: 20%;
  }
  .no-result {
    height: 400px;
  }
}
</style>
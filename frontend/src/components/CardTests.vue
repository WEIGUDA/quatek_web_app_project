<template>
  <div class="container">
    <div class="form-row search-row">
      <div class="input-group">
        <datetime
          v-model="datetime_from"
          type="datetime"
          input-class="form-control"
          format="yyyy-MM-dd HH:mm"
          :phrases="{ok: '确定', cancel: '取消'}"
          :minute-step="10"
        ></datetime>
        <label class="col-sm-1 text-center search-space">至</label>
        <datetime
          v-model="datetime_to"
          type="datetime"
          input-class="form-control"
          format="yyyy-MM-dd HH:mm"
          :phrases="{ok: '确定', cancel: '取消'}"
          :minute-step="10"
        ></datetime>
      </div>
      <div class="w-100">
        <br>
      </div>

      <div class="form-inline">
        <label class="sr-only" for="card_number">Query</label>
        <div class="input-group mb-2 mr-sm-2">
          <input
            name="card_number"
            type="text"
            class="form-control"
            v-model.trim="card_number"
            placeholder="卡号"
          >
        </div>

        <label class="sr-only" for="job_number">工号</label>
        <div class="input-group mb-2 mr-sm-2">
          <input
            name="job_number"
            type="text"
            class="form-control"
            v-model.trim="job_number"
            placeholder="工号"
          >
        </div>

        <label class="sr-only" for="department">部门</label>
        <div class="input-group mb-2 mr-sm-2">
          <input
            name="department"
            type="text"
            class="form-control"
            v-model.trim="department"
            placeholder="部门"
          >
        </div>

        <button
          type="submit"
          class="btn btn-success mb-2 btn_quatek"
          @click.prevent.stop="search()"
        >搜索</button>
      </div>
    </div>
    <div class="row btn-row">
      <p class="w-100 text-right">
        <button
          type="button"
          class="btn btn-secondary btn-row-btn btn-sm"
          title="下载"
          @click="download_excel()"
        >
          <!-- <font-awesome-icon icon="envelope" /> -->
          <font-awesome-icon icon="download"/>
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
            <th scope="col">卡号</th>
            <th scope="col">部门</th>
            <th scope="col">测试类型</th>
            <th scope="col">进出标志</th>
            <th scope="col">闸机id</th>
            <th scope="col">测试时间</th>
            <th scope="col">是否通过</th>
            <th scope="col">是否测试</th>
            <th scope="col">手腕检测值(KΩ)</th>
            <th scope="col">左脚检测值(KΩ)</th>
            <th scope="col">右脚检测值(KΩ)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cardtest in computed_cardtests" :key="cardtest._id.$oid">
            <td>{{cardtest.name}}</td>
            <td>{{cardtest.job_number}}</td>
            <td>{{cardtest.card_number}}</td>
            <td>{{cardtest.department}}</td>
            <td>{{cardtest.card_category}}</td>
            <td>{{cardtest.in_out_symbol}}</td>
            <td>{{cardtest.mc_id}}</td>
            <td>{{cardtest.test_datetime.$date | moment('YYYY-MM-DD HH:mm:ss')}}</td>
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
        <li class="page-item">
          <input
            class="page-link form-control go-to-page-number text-center"
            type="text"
            v-model="go_to_page_number"
          >
        </li>

        <li class="page-item">
          <a class="page-link" href="#" @click="go_to_page()">
            <span aria-hidden="true">Go</span>
            <span class="sr-only">Go</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import lodash from "lodash";
import fileDownload from "js-file-download";
import axios from "axios";
export default {
  name: "",
  data() {
    return {
      currentPage: 1,
      cardtests: [],
      query_string: "",
      datetime_from: this.$moment()
        .subtract(24, "hours")
        .second(0)
        .millisecond(0)
        .format("YYYY-MM-DDTHH:mm"),
      datetime_to: this.$moment()
        .add(12, "hours")
        .second(0)
        .millisecond(0)
        .format("YYYY-MM-DDTHH:mm"),
      cards: [],
      job_number: "",
      go_to_page_number: "",
      card_number: "",
      department: ""
    };
  },
  computed: {
    computed_cardtests: function() {
      let computed_cardtests = lodash.cloneDeep(this.cardtests);
      for (let cardtest of computed_cardtests) {
        let card = this.cards.filter(
          obj => obj.card_number === cardtest.card_number
        );
        if (card.length > 0) {
          cardtest.name = card[0].name;
          cardtest.job_number = card[0].job_number;
          cardtest.department = card[0].department;
        } else {
          let card2 = this.cards.filter(
            obj => String(obj.card_counter) === String(cardtest.card_counter)
          );
          if (card2.length > 0) {
            cardtest.name = card2[0].name;
            cardtest.job_number = card2[0].job_number;
            cardtest.department = card[0].department;
          } else {
            cardtest.name = "未找到姓名";
            cardtest.job_number = "未找到工号";
            cardtest.department = "未找到部门";
          }
        }
        if (cardtest.test_result === "0") {
          cardtest.test_result = "否";
        } else {
          cardtest.test_result = "是";
        }
        if (cardtest.is_tested === "0") {
          cardtest.is_tested = "否";
        } else {
          cardtest.is_tested = "是";
        }
        if (cardtest.card_category === "0") {
          cardtest.card_category = "VIP";
        } else if (cardtest.card_category === "1") {
          cardtest.card_category = "只测手";
        } else if (cardtest.card_category === "2") {
          cardtest.card_category = "只测脚";
        } else if (cardtest.card_category === "3") {
          cardtest.card_category = "手脚都测";
        }
        if (cardtest.in_out_symbol === "0") {
          cardtest.in_out_symbol = "出";
        } else if (cardtest.in_out_symbol === "1") {
          cardtest.in_out_symbol = "进";
        }
      }
      console.log(computed_cardtests);
      return computed_cardtests;
    }
  },
  methods: {
    search() {
      console.log(this.query_string);
      console.log(this.datetime_from);
      console.log(this.datetime_to);
      this.currentPage = 1;

      axios
        .get(
          `cardtests?q=${this.query_string}&datetime_from=${
            this.datetime_from
          }&datetime_to=${this.datetime_to}&job_number=${
            this.job_number
          }&card_number=${this.card_number}&department=${this.department}`
        )
        .then(response => {
          console.log(response.data);
          this.cardtests = response.data;
        })
        .catch(response => {
          console.log(response);
        });
    },

    download_csv() {
      if (this.cardtests.length > 0) {
        try {
          let title = "cardtests_page_" + this.currentPage;
          let cardtest_array = [];
          let csv_header =
            "id,card_number,name,job_number,card_category,in_out_symbol,gate_name,test_time,test_result,is_tested,hand_value,left_foot_value,right_foot_value\n";
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
                cardtest.right_foot
              ].join(",")
            );
          }
          csv = cardtest_array.join("\n");

          let uri =
            "data:text/csv;charset=utf-8," + csv_header + encodeURI(csv);

          let link = document.createElement("a");

          link.id = "csv-download-id";
          link.href = uri;

          document.body.appendChild(link);

          document.getElementById(link.id).style.visibility = "hidden";
          document.getElementById(link.id).download = title + ".csv";

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
        alert("没有数据可供下载!");
      }
    },

    download_excel() {
      axios
        .get(
          `cardtests?q=${this.query_string}&datetime_from=${
            this.datetime_from
          }&datetime_to=${this.datetime_to}&job_number=${
            this.job_number
          }&card_number=${this.card_number}&department=${
            this.department
          }&is_downloading_excel=true`,
          {
            responseType: "blob"
          }
        )
        .then(response => {
          console.log(response);
          fileDownload(
            response.data,
            "静电测试数据.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          );
        })
        .catch(response => {
          console.log(response);
        });
    },

    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      axios
        .get(
          `cardtests?offset=${offset}&q=${this.query_string}&datetime_from=${
            this.datetime_from
          }&datetime_to=${this.datetime_to}&job_number=${
            this.job_number
          }&card_number=${this.card_number}&department=${this.department}`
        )
        .then(response => {
          console.log(response.data);
          this.cardtests = response.data;
          this.currentPage--;
        })
        .catch(response => {
          console.log(response);
        });
    },

    nextPage() {
      let offset = this.currentPage * 50;
      axios
        .get(
          `cardtests?offset=${offset}&q=${this.query_string}&datetime_from=${
            this.datetime_from
          }&datetime_to=${this.datetime_to}&job_number=${
            this.job_number
          }&card_number=${this.card_number}&department=${this.department}`
        )
        .then(response => {
          if (response.data.length !== 0) {
            console.log(response.data);
            this.cardtests = response.data;
            this.currentPage++;
          } else {
            alert("已经到达最后一页!");
          }
        })
        .catch(response => {
          console.log(response);
        });
    },

    go_to_page() {
      this.currentPage = +this.go_to_page_number;
      let offset = this.currentPage - 1 * 50;
      axios
        .get(
          `cardtests?offset=${offset}&q=${this.query_string}&datetime_from=${
            this.datetime_from
          }&datetime_to=${this.datetime_to}&job_number=${
            this.job_number
          }&card_number=${this.card_number}&department=${this.department}`
        )
        .then(response => {
          if (response.data.length !== 0) {
            console.log(response.data);
            this.cardtests = response.data;
          } else {
            alert("该页面不存在!");
          }
        })
        .catch(response => {
          console.log(response);
        });
    }
  },

  created() {
    axios
      .get("cards?offset=0&limit=50000")
      .then(response => {
        console.log(response);
        this.cards = response.data;
      })
      .catch(response => {
        console.log(response);
      });
  }
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
.btn_quatek {
  background-color: #059c66;
}
.go-to-page-number {
  width: 50px;
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
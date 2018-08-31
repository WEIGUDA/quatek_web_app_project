<template>
  <div class="container">
    <div class="row search-row">
      <div class="input-group">
        <input type="text" class="form-control" aria-label="Search string" aria-describedby="basic-addon2" v-model.trim="query_string" placeholder="可搜索门禁类别">
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
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="导出" @click="download_csv()">
          <font-awesome-icon icon="download" />
        </button>
      </p>
    </div>

    <hr v-if="gates.length">
    <div class="row" v-if="!gates.length">
      <p class="w-100 text-center no-result">没有搜索到结果</p>
    </div>
    <div class="row" v-if="gates.length">
      <AppGate v-for="gate in gates" :gate=gate :key="gate._id.$oid"></AppGate>
    </div>
    <nav aria-label="Page navigation" v-if="gates.length">
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
    <b-modal v-model="show_modal" title="上传闸机信息" ok-only ok-title="上传" :lazy="true" @ok="upload()" ok-variant="success">
      <b-container fluid>
        <b-row>
          <a class="template_download" href="" @click.prevent="download_gates_upload_template()">闸机信息模版.csv</a>
        </b-row>
        <b-row>
          <b-form-file v-model="gates_upload_file" placeholder="请选择文件..." accept="text/csv"></b-form-file>
        </b-row>
        <b-row>

        </b-row>
      </b-container>

    </b-modal>
  </div>

</template>

<script>
import axios from 'axios';
import Gate from '@/components/Gate';

export default {
  name: 'Gates',
  data() {
    return {
      currentPage: 1,
      gates: [],
      query_string: '',
      show_modal: false,
      gates_upload_file: '',
    };
  },

  methods: {
    search() {
      console.log(this.query_string);

      axios
        .get(`gates?q=${this.query_string}`)
        .then((response) => {
          console.log(response);
          this.gates = response.data;
          this.currentPage = 1;
        })
        .catch((response) => {
          console.log(response);
        });
    },

    upload_show() {
      this.show_modal = true;
    },

    upload() {
      var reader = new FileReader();
      reader.onload = function(event) {
        let result = event.target.result;
        result = result.split('\n');
        for (let [index, item] of result.entries()) {
          result[index] = item.split(',');
        }
        console.log(result);
        axios
          .post('gates', result)
          .then((response) => {
            console.log(response);

            alert(`${response.data.result}台闸机信息上传成功!`);
          })
          .catch((response) => {
            console.log(response);
            alert('上传失败!');
          });
      };
      reader.readAsText(this.gates_upload_file);
    },

    download_gates_upload_template() {
      try {
        let title = 'gates_upload_template';
        let csv_header =
          '*gate_name,*gate_number,*gate_category,*mc_id,*hand_max,*hand_min,*foot_max,*foot_min,gate_ip,gate_port\n';
        let csv = [];
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
    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      axios
        .get(`gates?offset=${offset}&q=${this.query_string}`)
        .then((response) => {
          console.log(response);
          this.gates = response.data;
          this.currentPage--;
        })
        .catch((response) => {
          console.log(response);
        });
    },
    nextPage() {
      let offset = this.currentPage * 50;
      axios
        .get(`gates?offset=${offset}&q=${this.query_string}`)
        .then((response) => {
          if (response.data.length !== 0) {
            console.log(response);
            this.gates = response.data;
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
        let title = 'gates_page_' + this.currentPage;
        let gate_array = [];
        let csv_header =
          'id,name,number,category,mc_id,hand_max,hand_min,foot_max,foot_min,created_time,is_on,is_online\n';
        let csv = [];

        for (let gate of this.gates) {
          gate_array.push(
            [
              gate._id.$oid,
              gate.name,
              gate.number,
              gate.category,
              gate.mc_id,
              gate.hand_max,
              gate.hand_min,
              gate.foot_max,
              gate.foot_min,
              this.$moment(gate.created_time.$date).format(),
              gate.is_on,
              gate.is_online,
            ].join(','),
          );
        }
        csv = gate_array.join('\n');

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
    get_gates() {
      axios
        .get('gates')
        .then((response) => {
          console.log(response);
          this.gates = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
    },
  },
  components: {
    AppGate: Gate,
  },

  created() {
    this.get_gates();
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
.btn-row {
  text-align: center;
}
.btn-row-btn {
  margin: 0 5px;
  background-color: #868686;
}

.page-link {
  color: #059c66;
}
.template_download {
  color: #059c66;
  margin-bottom: 10px;
}
.btn-success {
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
  /* .btn-row {
    text-align: right !important;
  } */
  .search-row {
    margin: 0 -15px 20px -15px;
  }
  .no-result {
    height: 400px;
  }
}
</style>

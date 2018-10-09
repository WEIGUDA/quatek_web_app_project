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
    <b-modal v-model="show_modal" title="上传闸机信息" ok-only ok-title="上传" :lazy="true" @ok="upload2()" ok-variant="success">
      <b-container fluid>
        <b-row>
          <a class="template_download" href="" @click.prevent="download_gates_upload_template2()">闸机上传模版.xlsx</a>
        </b-row>
        <br>
        <b-row>
          <input type="file" name="excel_file" id="excel_file" ref="excel_file">
        </b-row>

      </b-container>

    </b-modal>

    <b-modal v-model="show_modal2" title="上传闸机信息" ok-only ok-title="查看详情" :lazy="true" @ok="routeToFailedUploadPage()" ok-variant="success">
      <b-container fluid>
        <b-row>
          {{this.last_upload_result.result}} 台闸机上传成功
        </b-row>
        <br>
        <b-row>
          {{this.last_upload_result.failed_numbers}} 台失败
        </b-row>

      </b-container>

    </b-modal>
  </div>

</template>

<script>
import axios from 'axios';
import fileDownload from 'js-file-download';
import Gate from '@/components/Gate';

export default {
  name: 'Gates',
  data() {
    return {
      currentPage: 1,
      gates: [],
      query_string: '',
      show_modal: false,
      file2: '',
      show_modal2: false,
      last_upload_result: {},
    };
  },

  methods: {
    search() {
      console.log(this.query_string);
      this.currentPage = 1;

      axios
        .get(`gates?q=${this.query_string}`)
        .then((response) => {
          console.log(response);
          this.gates = response.data;
        })
        .catch((response) => {
          console.log(response);
        });
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
        .post('upload_gates_excel', formData, {
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

    download_gates_upload_template2() {
      axios
        .get('download_gates_upload_template', {
          responseType: 'blob',
        })
        .then((response) => {
          console.log(response);
          fileDownload(
            response.data,
            '闸机上传模版.xlsx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          );
        })
        .catch((response) => {
          console.log(response);
        });
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
    FileReader,
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

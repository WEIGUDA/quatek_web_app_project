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
    <hr>
    <div class="row">
      <AppGate v-for="gate in gates" :gate=gate :key="gate._id.$oid"></AppGate>
    </div>
    <nav aria-label="Page navigation">
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
          <input type="file" class="form-control-file" @change="file_input_change($event)" accept="text/csv">
        </b-row>
        <b-row>

        </b-row>
      </b-container>

    </b-modal>
  </div>

</template>

<script lang="ts">
import Vue from 'vue';
import Gate from '@/components/Gate';
import axios from 'axios';
export default Vue.extend({
  data();,
});
</script>


<script>
import Vue from 'vue';
import Gate from '@/components/Gate';
import axios from 'axios';
export default Vue.extend({
  data();,
});
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
}
</style>

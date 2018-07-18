<template>
  <div class="container">

    <div class="row btn-row">
      <p class="w-100 text-right">
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
  </div>
</template>

<script>
import Gate from '@/components/Gate';

export default {
  name: 'Gates',
  data() {
    return {
      currentPage: 1,
      gates: null,
    };
  },
  methods: {
    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      this.$http.get(`gates?offset=${offset}`).then(
        (response) => {
          console.log(response.body);
          this.gates = response.body;
          this.currentPage--;
        },
        (response) => {
          console.log(response);
        },
      );
    },
    nextPage() {
      let offset = this.currentPage * 50;
      this.$http.get(`gates?offset=${offset}`).then(
        (response) => {
          if (response.body.length !== 0) {
            console.log(response.body);
            this.gates = response.body;
            this.currentPage++;
          } else {
            alert('已经到达最后一页!');
          }
        },
        (response) => {
          console.log(response);
        },
      );
    },

    download_csv() {
      try {
        let title = 'gates';
        let gate_array = [];
        let csv_header = 'id,name,number,category,hand_max,hand_min,foot_max,foot_min,created_time,is_on,is_online\n';
        let csv = [];

        for (let gate of this.gates) {
          gate_array.push(
            [
              gate._id.$oid,
              gate.name,
              gate.number,
              gate.category,
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
  },
  components: {
    AppGate: Gate,
  },

  created() {
    this.$http.get('gates').then(
      (response) => {
        console.log(response.body);
        this.gates = response.body;
      },
      (response) => {
        console.log(response);
      },
    );
  },
};
</script>

<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
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
  .btn-row {
    text-align: right !important;
  }
}
</style>

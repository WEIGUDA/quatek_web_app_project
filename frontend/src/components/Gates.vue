<template>
    <div class="container">

        <div class="row btn-row">
            <p class="w-100 text-right">
                <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="导出">
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
                    <a class="page-link" href="#" aria-label="Previous" @click="prevPage(currentPage)">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">上一页</span>
                    </a>

                </li>
                <li class="page-item disabled">
                    <a class="page-link">第 {{currentPage}} 页</a>
                </li>

                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Next" @click="nextPage(currentPage)">
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
    prevPage(currentPage) {
      let offset = (currentPage - 2) * 50;
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
    nextPage(currentPage) {
      let offset = currentPage * 50;
      this.$http.get(`gates?offset=${offset}`).then(
        (response) => {
          console.log(response.body);
          this.gates = response.body;
          this.currentPage++;
        },
        (response) => {
          console.log(response);
        },
      );
    },
  },
  props: {},
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

    // this.$http.post('gates', { foo: 'bar' }).then(
    //   (response) => {
    //     console.log(response.body);
    //   },
    //   (response) => {
    //     console.log(response);
    //   },
    // );
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

<template>
    <div class="container">
        <div class="row search-row">
            <div class="input-group">
                <input type="text" class="form-control" aria-label="Search string" aria-describedby="basic-addon2" v-model="query_string">
                <div class="input-group-append">
                    <button class="btn btn-outline-success btn-outline-quatek" type="button" @click="search()">
                        <font-awesome-icon icon="search" /> Search</button>
                </div>
            </div>
        </div>
        <div class="row btn-row">
            <p class="w-100 text-right">
                <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="上传">
                    <font-awesome-icon icon="upload" />
                </button>
                <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="下载">
                    <font-awesome-icon icon="download" />
                </button>
                <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="添加卡片" @click="cardAdd()">
                    <font-awesome-icon icon="user-plus" />
                </button>
            </p>
        </div>
        <div class="row">
            <table class="table table-striped table-responsive-md">
                <thead>
                    <tr>
                        <th scope="col">姓名</th>
                        <th scope="col">工号</th>
                        <th scope="col">卡号</th>
                        <th scope="col">卡类型</th>
                        <th scope="col">部门</th>
                        <th scope="col">修改</th>
                        <th scope="col">删除</th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="card in cards" :key="card._id.$oid">
                        <td>{{card.name}}</td>
                        <td>{{card.job_number}}</td>
                        <td>{{card.card_number}}</td>
                        <td>{{card.card_category}}</td>
                        <td>{{card.department}}</td>
                        <td>
                            <button type="button" class="btn btn-secondary btn-quatek btn-sm">
                                <font-awesome-icon icon="pencil-alt" />
                            </button>
                        </td>
                        <td>
                            <button type="button" class="btn btn-secondary btn-quatek btn-sm">
                                <font-awesome-icon icon="trash-alt" />
                            </button>
                        </td>
                    </tr>
                </tbody>

            </table>
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
export default {
  name: 'Cards',
  data() {
    return {
      currentPage: 1,
      cards: null,
      query_string: '',
    };
  },
  computed: {
    q() {
      return this.query_string.trim();
    },
  },
  methods: {
    cardAdd() {
      this.$router.push({ name: 'CardCreate' });
    },
    search() {
      console.log(this.query_string);

      this.$http.get(`cards?q=${this.q}`).then(
        (response) => {
          console.log(response.body);
          this.cards = response.body;
          this.currentPage = 1;
        },
        (response) => {
          console.log(response);
        },
      );
    },
    prevPage() {
      let offset = (this.currentPage - 2) * 50;
      this.$http.get(`cards?offset=${offset}&q=${this.q}`).then(
        (response) => {
          console.log(response.body);
          this.cards = response.body;
          this.currentPage--;
        },
        (response) => {
          console.log(response);
        },
      );
    },
    nextPage() {
      let offset = this.currentPage * 50;
      this.$http.get(`cards?offset=${offset}&q=${this.q}`).then(
        (response) => {
          if (response.body.length !== 0) {
            console.log(response.body);
            this.cards = response.body;
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
  },
  created() {
    this.$http.get('cards').then(
      (response) => {
        console.log(response.body);
        this.cards = response.body;
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
}
</style>


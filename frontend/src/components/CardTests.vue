<template>
    <div class="container">
        <div class="row search-row">
            <div class="input-group">
                <input type="text" class="form-control" aria-label="Search string" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <button class="btn btn-outline-success btn-outline-quatek" type="button">
                        <font-awesome-icon icon="search" /> Search</button>
                </div>
            </div>
        </div>
        <div class="row btn-row">
            <p class="w-100 text-right">
                <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="email发送测试">
                    <font-awesome-icon icon="envelope" />
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

                    <tr v-for="card in 25" :key="card">
                        <td>姓名1</td>
                        <td>12938475</td>
                        <td>384758692747387</td>
                        <td>卡类型1</td>
                        <td>部门1</td>
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
                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Previous">
                        <span aria-hidden="true">
                            <font-awesome-icon icon="caret-square-left" /> </span>
                        <span class="sr-only">上一页</span>
                    </a>

                </li>
                <li class="page-item disabled">
                    <a class="page-link">第 {{currentPage}} 页</a>
                </li>

                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Next">
                        <span aria-hidden="true">
                            <font-awesome-icon icon="caret-square-right" /> </span>
                        <span class="sr-only">下一页</span>
                    </a>
                </li>

            </ul>
        </nav>
    </div>
</template>

<script>
export default {
  name: '',
  data: function() {
      return {
          
      };
  },
  props: {
 
  }
}
</script>



<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.search-row {
  margin-bottom: 20px;
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
}
</style>
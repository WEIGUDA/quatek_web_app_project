<template>
    <div class="container">
        <div class="row btn-row">
            <p class="w-100">
                <button type="button" class="btn btn-success btn-quatek btn-sm">LOG导出</button>
            </p>
        </div>
        <div class="row">
            <app-gate v-for="gate in 10" :key="gate"></app-gate>
        </div>
        <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm justify-content-center">
                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">上一页</span>
                    </a>

                </li>
                <li class="page-item disabled">
                    <a class="page-link">第 {{currentPage}} 页</a>
                </li>

                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Next">
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
  data: function() {
      return {
          currentPage: 1,
          
      };
  },
  props: {
 
  },
  components: {
      AppGate: Gate,
  }
}
</script>

<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.btn-row {
  text-align: center;
}
.btn-quatek {
  background-color: #059c66;
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

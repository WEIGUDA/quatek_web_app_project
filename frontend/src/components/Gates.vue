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
    </div>
</template>

<script>
import Gate from '@/components/Gate';
export default {
  name: 'Gates',
  data: function() {
      return {
          
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

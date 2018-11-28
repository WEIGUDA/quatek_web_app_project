<template>
  <div>
    <div>
      <label>1. HID 卡号转换</label>
      <br>
      <small>请将 HID 卡号放在 Excel 文件的第一列</small>
      <br>
      <br>
      <input
        type="file"
        name="hid_excel_file"
        id="hid_excel_file"
        ref="hid_excel_file"
      >
      <button @click.prevent.stop="submit_hid_excel_file()">提交</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import fileDownload from "js-file-download";
export default {
  data() {
    return {
      //
    };
  },
  methods: {
    submit_hid_excel_file() {
      let formData = new FormData();
      let excel_file = this.$refs.hid_excel_file.files[0];
      formData.append("hid_excel_file", excel_file);
      axios
        .post("/hid_card_convertor", formData, {
          responseType: "blob",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          console.log(response.data);
          fileDownload(
            response.data,
            "HID转换.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          );
        })
        .catch(response => {
          console.log(response);
        });
    }
  }
};
</script>


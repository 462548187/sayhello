<template>
  <el-container>
    <el-header>
      <a href="/project/message">
        <strong>Say Hello</strong>
      </a>
      <small>to the world</small>
    </el-header>
    <el-main>
      <!--姓名 -->
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-position="top"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model.trim="ruleForm.name" maxlength="12" autocomplete="off"></el-input>
        </el-form-item>
        <!--手机-->
        <el-form-item label="手机" prop="phone">
          <el-input v-model.trim="ruleForm.phone" maxlength="11" autocomplete="off"></el-input>
        </el-form-item>

        <!--内容 -->
        <el-form-item label="消息" prop="desc">
          <el-input type="textarea" v-model.trim="ruleForm.desc" maxlength="200" autocomplete="off"></el-input>
        </el-form-item>

        <!--提交、重置 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button type="primary" @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>

      <p class="total">{{messageTotal}} 消息</p>
      <div class="list-groups" v-for="message in messages">
        <div class="list-group">
          <div class="item-header">
            {{message.name}}
            <small class="m-1">#{{message.id}}</small>
            <div>
              <small class="m-2">{{message.create_at}}</small>
            </div>
          </div>
          <p>{{message.body}}</p>
        </div>
      </div>

      <!-- 分页 -->
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="page"
        :page-size="pageSize"
        :total="messageTotal"
        :hide-on-single-page="show"
        @current-change="handleCurrentChange1"
      ></el-pagination>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data () {
    return {
      messageTotal: 0,
      messages: [],
      show: true,
      result: false,
      // 请求数据的页码
      page: 1,
      pageSize: 5,

      ruleForm: {
        name: '',
        phone: '',
        desc: ''
      },
      rules: {
        name: [{
          required: true,
          message: '请输入姓名',
          trigger: 'change'
        },
        {
          min: 2,
          max: 12,
          required: true,
          pattern: /^[\u0391-\uFFE5A-Za-z]+$/,
          message: '长度在 2 到 12 个汉字或英文',
          trigger: 'change'
        }
        ],
        desc: [{
          required: true,
          message: '请输入留言内容',
          trigger: 'change'
        },
        {
          min: 1,
          max: 200,
          message: '长度在 1 到 200 个字符',
          trigger: 'change'
        }
        ],
        phone: [{
          required: true,
          message: '请输入手机号码',
          trigger: 'change'
        }, {
          required: true,
          pattern: /^1[3456789]\d{9}$/,
          message: '请输入正确手机号码',
          trigger: 'change'
        }
        ]
      }
    };
  },
  methods: {
    async getData () {
      await this.$axios.get('/message', {
        params: {
          page: this.page, // 页码
        }
      })
        .then(response => {
          this.messageTotal = response.data.total,
            this.messages = response.data.data,
            console.log("get")
        })
        .catch(err => { // 请求失败处理
          console.log(err);
        });
    },

    async postData () {
      await this.$axios.post('/message', {
        name: this.ruleForm.name,
        phone: this.ruleForm.phone,
        body: this.ruleForm.desc
      }).then(response => {
        console.log("post请求")
        this.$message({
          message: '感谢您的留言~',
          type: 'success'
        })
        // 清空输入框
        this.getData()
        this.resetForm("ruleForm")
      }).catch(error => {
        this.$message.error('请求错误!')
      });
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.postData()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm (formName) {
      this.$refs[formName].resetFields();
    },
    handleCurrentChange1: function (currentPage) { //页码切换
      this.page = currentPage
      this.getData()
    }
  },
  mounted () {
    this.getData(this.page)
  }
}
</script>

<style>
body {
  background-color: rgb(245, 245, 245) !important;
}

header {
  margin: 50px 0 40px 0;
}

footer {
  margin: 20px;
}

.el-header,
.el-footer {
  /* background-color: #B3C0D1;
    color: #333; */
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  width: 80%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.el-footer > div {
  display: inline;
}

.el-header > div {
  display: inline;
}

.el-form {
  width: 50%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

strong {
  font-size: 3.5rem;
  font-weight: 300;
  line-height: 1.2;
  color: #28a745 !important;
}

a {
  text-decoration: none !important;
}

small {
  font-size: 24px;
  font-weight: 400;
  color: #6c757d !important;
}

.el-textarea__inner {
  height: 85px;
}

/* 提交表单样式 */
.el-form--label-top .el-form-item__label {
  float: left;
  padding: 0px;
}

.total {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  font-family: inherit;
  font-weight: 500;
  line-height: 1.2;
  color: inherit;
  margin-left: 25%;
}

.list-groups {
  width: 50%;
  margin-right: auto;
  margin-left: auto;
}

/* 列表展示还有问题 圆角 */
.list-group {
  position: relative;
  display: block;
  padding: 0.75rem 1.25rem;
  margin-bottom: -1px;
  background-color: #fff;
  border-top-left-radius: 0.25rem;
  border-top-right-radius: 0.25rem;
  border-radius: 1px solid rgba(0, 0, 0, 0.125);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.list-group > div {
  color: #28a745 !important;
  margin-bottom: 0.25rem !important;
  font-size: 1.25rem;
  text-align: left;
  line-height: 100%;
}

.list-group > div > div {
  display: inline;
  float: right;
}

.m-1 {
  color: #6c757d !important;
  font-size: 80%;
}

.m-2 {
  font-size: 30%;
  font-weight: 400;
}

p {
  margin-bottom: 0.25rem !important;
  text-align: left;
  line-height: 100%;
}

/* 分页 */
.el-pagination {
  line-height: initial;
}
</style>

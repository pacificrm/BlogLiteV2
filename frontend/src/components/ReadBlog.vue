<template>
  <div class="ffblog">
    <NavBar :username="this.username"></NavBar>
    <div class="tbg">
      <h1><span v-html="this.Blogdata.blogTitle"> </span></h1>
    </div>
    <div class="eng">
      <router-link class="b" :to="`/postengage/${this.bgid}`"
        >Post-Engagement</router-link
      >
    </div>
    <div class="hmm"><a href="/home">Home</a></div>
    <div class="cbg"><span v-html="this.Blogdata.blogContent"> </span></div>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "ReadBlog",
  components: {
    NavBar,
  },
  data() {
    return {
      Blogdata: {
        blogTitle: null,
        blogPrev: null,
        blogContent: null,
        blogImage: null,
      },
      username: null,
      auth_token: null,
      bgid: null,
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.username = sessionStorage.getItem("username");
    this.bgid = this.$route.params.id;
    // console.log(this.email)
    if (!this.auth_token) {
      alert("Please Login to see your dashboard.");
      this.$router.push("/");
    }
    return fetch(`http://127.0.0.1:5000/api/blog/${this.bgid}`, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authentication-Token": `${this.auth_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.Blogdata.blogTitle = data["title"];
        this.Blogdata.blogPrev = data["preview"];
        this.Blogdata.blogContent = data["content"];
        console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
  //   methods: {
  //     async engage(id) {
  //       this.$router.push(`/postengage/${id}`);
  //     },
  //   },
};
</script>
<style>
.ffblog {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
    url("../assets/ss2.jpg") no-repeat center/cover;
  /* border: 1px solid red; */
  width: 100vw;
  min-height: 100vh;
  overflow: auto;
  position: relative;
}
.tbg {
  /* border: 1px solid blue; */
  color: rgb(240, 219, 129);
  width: 99%;
  top: 150px;
  max-height: 200px;
  min-height: 200px;
  position: absolute;
  text-align: center;
  font-size: 1.5rem;
  overflow: auto;
  /* font-family: "Yeon Sung", cursive; */
  font-family: "Rowdies", cursive;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #e90101;
}

.eng,
.hmm {
  color: black;
  display: block;
  position: absolute;
  top: 100px;
  border: 1px solid red;
  font-size: 1.2rem;
  background: #f7f2ff;
  box-shadow: 0px 2px 6px #00e8fd;
}

.eng {
  left: 10px;
}
.hmm {
  right: 10px;
}
.eng a,
.hmm a {
  font-family: "Rubik Bubbles", cursive;
  color: black;
  text-decoration: none;
}
.eng a:hover {
  background: #555252;
  color: #d8d4d4;
}
.hmm a:hover {
  background: #555252;
  color: #d8d4d4;
}

.cbg {
  color: #ffffff;
  /* border: 2px solid green; */
  top: 350px;
  max-height: 350px;
  min-height: 350px;
  /* min-width: 800px; */
  overflow: auto;
  position: absolute;
  padding: 20px;
  font-size: 1.5rem;
  /* display: inline-block; */
  font-family: "Yeon Sung", cursive;
  -webkit-text-stroke-width: 1px;
  /* -webkit-text-stroke-color: #08fcf0; */
}
</style>

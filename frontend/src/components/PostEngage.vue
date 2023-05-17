<template>
  <div class="engage">
    <NavBar :username="this.username"></NavBar>
    <router-link class="bck" :to="`/readblog/${this.bgid}`">Back </router-link>
    <img src="@/assets/test.png" alt="No image" />
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "PostEngage",
  components: {
    NavBar,
  },
  data() {
    return {
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
        // this.Blogdata.blogTitle = data["title"];
        // this.Blogdata.blogPrev = data["preview"];
        // this.Blogdata.blogContent = data["content"];
        console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
};
</script>

<style scoped>
.engage {
  /* border: 1px solid #ff0000; */
  position: relative;
  min-height: 100vh;
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6));
}
.engage img {
  display: block;
  position: absolute;
  left: 380px;
  top: 120px;
  border: 1px solid rebeccapurple;
  box-shadow: 0px 5px 15px #00ebfc;
  height: 550px;
  width: 800px;
}

.bck {
  text-decoration: none;
  display: block;
  color: azure;
  position: absolute;
  right: 10px;
  top: 80px;
  /* font-weight: 800; */
  font-size: 1.5rem;
  font-family: "Rubik Spray Paint", cursive;
  border-radius: 20px;
  box-shadow: 0px 2px 6px #5ce7ff;
  padding: 8px;
}
.bck:hover {
  background: #3b3a3a;
}
</style>

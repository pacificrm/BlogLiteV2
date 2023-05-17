<template>
  <header>
    <div class="logo">
      <h1 class="logo-text"><span>Blog</span>Lite</h1>
    </div>
    <ul>
      <li><a href="/home">Home</a></li>
      <li>
        <a href="/searchuser">Search</a>
        <!-- <ul style="left: 0px">
          <li><a href="/searchuser">By User-Name</a></li>
          <li><a href="/search/fullname">By Full-name </a></li>
        </ul> -->
      </li>
      <li>
        <a href="/postblog">
          <!-- <i class="fa fa-search" style="color: white; font-size: 0.8em"></i> -->
          <!-- <i class="fa fa-magnifying-glass"></i> -->
          Post-Blog
        </a>
      </li>
      <li>
        <a v-bind:href="'/profile/' + this.username">
          Profile
          <!-- <router-link to="`/profile/${this.username}`">Profile</router-link> -->
          <!-- <i class="fa fa-search" style="color: white; font-size: 0.8em"></i> -->
          <!-- <i class="fa fa-magnifying-glass"></i> -->
          <router-view></router-view>
        </a>
        <router-view></router-view>
      </li>

      <li>
        <a href="#">
          <i class="fa fa-user"></i>
          {{ this.username }}
          <i class="fa fa-chevron-down" style="font-size: 0.8em"></i>
        </a>
        <ul>
          <!-- <li><a href="#" @click="dele()">Delete-user</a></li> -->
          <li><a href="/" @click="lout()">Logout</a></li>
        </ul>
      </li>
    </ul>
  </header>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    username: {
      default: "",
    },
    data() {
      return {
        currusername: null,
        auth_token: null,
      };
    },
    async created() {
      this.auth_token = sessionStorage.getItem("auth-token");
      this.currusername = sessionStorage.getItem("username");
      console.log(this.currusername);
      if (!this.auth_token) {
        alert("Please Login to see your dashboard.");
        this.$router.push("/");
      }
    },

    methods: {
      async lout() {
        console.log("clear");
        sessionStorage.clear();
        localStorage.clear();
        this.$router.push("/");
      },
      // async dele() {
      //   if (confirm("Want to delete this user !!")) {
      //     const res = await fetch(`http://127.0.0.1:5000/api/user/`, {
      //       method: "DELETE",
      //       mode: "cors",
      //       headers: {
      //         "Content-Type": "application/json",
      //         "Access-Control-Allow-Origin": "*",
      //         "Authentication-Token": `${this.auth_token}`,
      //       },
      //     });
      //     if (res.ok) {
      //       sessionStorage.clear();
      //       localStorage.clear();
      //       this.$router.push("/");
      //       window.location.reload();
      //       console.log("commentd");
      //       // this.success = "Followed.";
      //     } else if (res.status === 400) {
      //       console.log("error!!");
      //     }
      //     console.log("You pressed OK!");
      //   } else {
      //     console.log("You pressed Cancel!");
      //     this.$router.go();
      //     window.location.reload();
      //   }
      // },
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Candal&display=swap");
header {
  background: url("../assets/s4.png") no-repeat center / cover;
  /* background: #a665fc; */
  height: 66px;
  /* position: fixed; */
  /* color: white; */
}
header * {
  color: white;
}

header .logo {
  float: left;
  height: inherit;
  margin-left: 2em;
}

header .logo-text {
  margin: 9px;
  /* margin-left: 0px; */
  font-family: "candal", "sans-serif";
}

header .logo-text span {
  color: #13e3f7;
}

header ul {
  float: right;
  /* border: 21px solid red; */
  margin: 0px;
  padding: 0px;
  list-style: none;
  height: inherit;
  /* overflow: hidden; */
  /* border: 1px solid red; */
}

header ul li {
  float: left;
  position: relative;
  /* border: 1px solid red; */
}

header ul li a {
  display: block;
  padding: 20px;
  font-size: 1.3em;
  text-decoration: none;
  height: inherit;
}

header ul li a:hover {
  /* background: #6a27b6; */
  background: #47079c;
  transition: 0.5s;
}

header ul li ul {
  position: absolute;
  top: 66px;
  right: 0px;
  width: 180px;
  display: none;
}

header ul li:hover ul {
  display: block;
}

header ul li ul li {
  width: 100%;
  z-index: 10;
}

header ul li ul li a {
  padding: 10px;
  background: white;
  color: #575656;
}
header ul li ul li a:hover {
  color: red;
}
header ul li ul li a:hover {
  background: #d8d4d4;
}
</style>

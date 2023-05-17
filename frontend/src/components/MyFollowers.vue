<template>
  <div class="all">
    <NavBar :username="this.username"></NavBar>
    <div class="follows">
      <ul>
        <li v-for="fl of follower" :key="fl.uid">
          <router-link class="lbt" :to="`/profile/${fl['uid']}`">{{
            fl["username"]
          }}</router-link>
          <!-- <a class="lbt" href="/profile/{{i[0]}}"> {{ "i[1]" }} </a> -->
          <a class="fbt" href="#" @click="unfollow(fl['username'])" id="ufl">
            Unfollow
          </a>
          <a class="fbt" href="#" @click="follow(fl['username'])" id="fl">
            Follow
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "MyFollowers",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      //   about: null,
      //   email: null,
      auth_token: null,
      // lists: {},
      follower: null,
      //   profile_pic: null,
      error: "",
      success: "",
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.username = sessionStorage.getItem("username");
    // console.log(this.email)
    if (!this.auth_token) {
      alert("Please Login to see your dashboard.");
      this.$router.push("/");
    }
    return fetch(`http://127.0.0.1:5000/api/user`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.follower = data["follower"];
        // this.email = data["email"];
        // this.fullname = data["fullname"];
        // this.about = data["about"];
        console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
  methods: {
    async follow(user) {
      this.success = null;
      this.error = null;
      const res = await fetch(`http://127.0.0.1:5000/api/follow`, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication-Token": `${this.auth_token}`,
        },
        body: JSON.stringify({
          follower: this.username,
          following: user,
          is_authenticated: true,
        }),
      });
      if (res.ok) {
        this.$router.go();
        window.location.reload();
        console.log("registered");
        this.success = "Followed.";
      } else if (res.status === 400) {
        this.success = "You allready follow this user!!";
      }
    },
    async unfollow(user) {
      this.error = null;
      this.success = null;
      // var c = localStorage.getItem("suser");
      // this.fuser = localStorage.getItem("suser");
      // console.log(c);
      const res = await fetch(`http://127.0.0.1:5000/api/unfollow`, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication-Token": `${this.auth_token}`,
        },
        body: JSON.stringify({
          follower: this.username,
          unfollowing: user,
          is_authenticated: true,
        }),
      });
      if (res.ok) {
        console.log("registered");
        this.error = "Unfollowed!!";
      } else if (res.status === 400) {
        this.error = "You are not following this user!!";
      }
    },
  },
};
</script>

<style scoped>
.follows {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    no-repeat center/cover;
  /* border: 1px solid red; */
  /* url("../assets/pp10.jpeg") */
  min-height: 91vh;
  /* height: 90%; */
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  /* overflow: hidden; */
}

.follows ul {
  /* border: 1px solid blue; */
  position: relative;
  width: 700px;
  min-height: 70vh;
  list-style: none;
  color: #f5f2f2;

  /* display: flex;
  flex-direction: row; */
}

.follows li {
  /* margin-top: 0px;
  padding-top: 0px; */
  font-size: 1.5rem;
  /* border: 1px solid green; */
  /* position: absolute; */
  width: 90%;
  margin-top: 20px;
  font-weight: bold;
  display: inline-block;
  color: white;
  /* font-family: "Titan One", cursive; */
  -webkit-text-stroke-width: 1px;
  /* -webkit-text-stroke-color: #cd06ff; */
}
.lbt {
  color: white;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #cd06ff;
  text-decoration: none;
  font-size: 2.2rem;
  font-weight: bold;
  float: left;
  margin-top: 0px;
  padding-top: 0px;
}

.fbt {
  font-size: 1.4rem;
  float: right;
  margin-right: 25px;
  text-decoration: none;
  display: block;
  border-radius: 30px;
  width: 120px;
  font-family: "Rubik Spray Paint", cursive;
  text-align: center;
  /* padding: 2px; */
  color: #0f5c63;
  font-weight: normal;

  background: #e6e4e4;
  -webkit-text-stroke-width: 0px;
  /* -webkit-text-stroke-color: black; */
  margin-top: 10px;
}

.fbt:hover {
  box-shadow: 1px 1px 2px #d0bfe6;
}
</style>

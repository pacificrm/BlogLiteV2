<template>
  <div class="search">
    <NavBar :username="this.username"></NavBar>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css"
    />
    <div class="popup">
      <p class="alert alert-danger alert-dismissible fade show" v-if="error">
        {{ error
        }}<button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </p>
      <p
        class="alert alert-success alert-dismissible fade show"
        role="alert"
        v-if="success"
      >
        {{ success
        }}<button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </p>
      <!-- <div class="alert alert-danger alert-dismissible fade show" role="alert">
        helllo
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div> -->
    </div>

    <div class="searcharea">
      <form class="searchbox" action="" method="POST">
        <input
          type="text"
          v-model="this.susername"
          placeholder="Search....."
          required
        />
        <!-- <input type="submit" value="search" /> -->
        <button type="submit" @click.prevent="search()">
          <i class="fas fa-search"></i>
        </button>
        <i class="fa fa-magnifying-glass"></i>
        <i class="fa-solid fa-magnifying-glass"></i>
      </form>
    </div>

    <div v-if="users" class="search-result">
      <ul>
        <li v-for="user of this.users" :key="user">
          <a @click="usr(user['username'])" class="lst" href="#"
            >{{ user["username"] }}
          </a>
          <a
            class="sbt"
            v-if="!(user['username'] == this.username)"
            href="#"
            id="ufl"
            @click.prevent="unfollow(user['username'])"
          >
            unfollow
          </a>
          <a
            class="sbt"
            v-if="!(user['username'] == this.username)"
            href="#"
            id="fl"
            @click.prevent="follow(user['username'])"
          >
            follow
          </a>
          <!-- {% else %}
          <a class="sbt" href="/nunfollow/{{i['id']}}" id="ufl"> unfollow </a>
          <a class="sbt" href="/nfollow/{{i['id']}}" id="fl"> follow </a>
          {% endif %} -->
        </li>
      </ul>
      <!-- <ul>
        
        <li>
          <a class="lst" href="/profile/{{i['user_id']}}"
            >{{ i["fullname"] }}
          </a>
          {% if i['id'] != current_user.id %} {% if f %}
          <a class="sbt" href="/funfollow/{{i['user_id']}}" id="ufl">
            unfollow
          </a>
          <a class="sbt" href="/ffollow/{{i['user_id']}}" id="fl"> follow </a>
          {% else %}
          <a class="sbt" href="/nunfollow/{{i['user_id']}}" id="ufl">
            unfollow
          </a>
          <a class="sbt" href="/nfollow/{{i['user_id']}}" id="fl"> follow </a>
          {% endif %}
        </li>
        {% endif %} {% endfor %}
      </ul>
      {% endif %} -->
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
// import { create } from "domain";
export default {
  name: "SearchUser",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      // fullname: null,
      // email: null,
      susername: null,
      auth_token: null,
      users: null,
      // fluser: null,
      // ufuser: null,
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
  },
  methods: {
    async usr(user) {
      this.$router.push(`/profile/${user}`);
    },
    async search() {
      fetch(`http://127.0.0.1:5000/api/search`, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication-Token": `${this.auth_token}`,
        },
        body: JSON.stringify({
          username: this.susername,
          is_authenticated: true,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          // this.email = data["email"];
          // this.username = data["fullname"];
          this.users = data["users"];
          console.log(data["users"]);
          for (var i of data["users"]) {
            console.log(i["username"]);
          }
        })
        .catch((error) => console.log("1st", error));
    },
    // async flsetuser(user) {
    //   // localStorage.clear();
    //   // localStorage.setItem("fluser", user);
    //   // this.fluser = localStorage.getItem("fluser");
    //   this.fluser = user;
    //   console.log(this.fluser);
    // },
    // async ufsetuser(user) {
    //   // localStorage.clear();
    //   // localStorage.setItem("fluser", user);
    //   // this.fluser = localStorage.getItem("fluser");
    //   this.ufuser = user;
    //   console.log(this.ufuser);
    // },
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
.search {
  /* margin: 20px;
  width: 700px; */
  /* border: 1px solid red; */
  /* display: flex; */
  /* align-items: center; */
  /* justify-content: center; */
  position: relative;
  min-height: 100vh;
  min-width: 700px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("../assets/s1.png") no-repeat center/cover;
}

.popup {
  position: absolute;
  text-align: center;
  /* top: 10px; */
  /* left: 370px;
  width: 770px; */
  display: fixed;
  /* justify-content: center; */
  /* border: 1px solid red; */
  max-height: 60px;
  /* border-radius: 60px; */
  overflow: hidden;
  /* background: transparent; */
  width: 100%;
}

.searcharea {
  position: absolute;
  /* border: 1px solid rgb(60, 255, 0); */
  top: 200px;
  left: 430px;
  width: 700px;
  display: flex;
  justify-content: center;
  border-radius: 60px;
  padding: 0px;
  background: rgb(224, 224, 224);
  overflow: hidden;
  max-height: 50px;
  box-shadow: 1px 1px 2px grey;
}
/* .searcharea:hover {
  box-shadow: 1px 1px 2px rgb(7, 231, 212);
} */
.searchbox input {
  width: 630px;
  /* border: 1px solid rgb(212, 208, 216); */
  height: 100%;
  background: transparent;
  border: 0px;
  outline: 0px;
  margin-left: 10px;
  font-size: 1.4rem;
}
.searchbox button {
  width: 40px;
  /* border: 1px solid rgb(216, 59, 11); */
  margin: 0px;
  height: 100%;
  font-size: 1.5rem;
  border: 0px;
  outline: 0px;
  padding: 0px;
  background: transparent;
}
.search-result {
  position: absolute;
  /* border: 1px solid rgb(236, 245, 236); */
  bottom: 0px;
  top: 250px;
  width: 700px;
  left: 440px;
  /* margin: 50px; */
}
.search-result ul {
  /* border: 1px solid red; */
  list-style: none;
  height: 100%;
  overflow: auto;
}
.search-result ul li {
  /* border: 1px solid green; */
  margin: 4px 0px;
  height: 40px;
  font-size: 1.6rem;
  /* font-family: "Titan One", cursive; */
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #ebe5f1;

  color: white;
}

.lst {
  font-size: 1.8rem;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #ffc402;
  float: left;
  text-decoration: none;
  color: wheat;
  font-weight: bold;
}

.sbt {
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
  color: #47079c;

  background: #f5f2f2;
  -webkit-text-stroke-width: 0px;
  /* -webkit-text-stroke-color: black; */
}

.sbt:hover {
  box-shadow: 1px 1px 2px 2px #e8e2e9;
}

#fl:hover {
  background-color: green;
  color: rgb(255, 255, 255);
}
#ufl:hover {
  background-color: red;
  color: rgb(255, 255, 255);
}
</style>

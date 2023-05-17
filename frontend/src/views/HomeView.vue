<template>
  <div class="home">
    <NavBar :username="this.username"></NavBar>
    <div class="content-area">
      <div class="content">
        <div class="head-nav">
          <!-- <input type="submit" value="Recent Posts" />
        <input id="post" type="submit" value="Post-Blog" /> -->
          <a href="#"> Recent Posts </a>
          <!-- <a href="/user/postBlog"> Post-Blog </a> -->
        </div>
        <div v-if="this.blogs" class="allposts">
          <div v-for="blog of blogs" :key="blog.id" class="posts">
            <!-- <input  type="checkbox" class="chk" aria-hidden="true" />
        <div class="content">
        <div class="p"> -->
            <img
              :src="require(`@/assets/blogs/${blog.image}`)"
              alt="Post Image"
              class="post-image"
            />
            <div class="post-preview">
              <h1>
                <span v-html="blog['title']"></span>
              </h1>

              <div
                class="info"
                style="position: absolute; font-size: 1.2rem; top: 85px"
              >
                <i id="usr" class="far fa-user" @click="usr(blog['user'])">
                  {{ blog["user"] }}
                </i>

                &nbsp;
                <i id="dt" class="fa fa-calendar"
                  >{{ blog["date"] }}&nbsp;&nbsp;{{ blog["time"] }}</i
                >
              </div>

              <p class="preview-text">
                <span v-html="blog['preview']"></span>
              </p>
              <div class="intr">
                {{ blog["likes"] }}
                <i class="fa fa-thumbs-up lk" @click="like(blog['id'])"> </i
                >&nbsp;&nbsp; {{ blog["dislikes"] }}
                <i class="fa fa-thumbs-down lk" @click="unlike(blog['id'])">
                </i>
                &nbsp;&nbsp;{{ blog["comments"] }}
                <i class="fa fa-comment cmnt" @click="comment(blog['id'])"></i>
              </div>

              <a href="#" class="btn" @click.prevent="readblog(blog['id'])"
                >Read More</a
              >
            </div>
          </div>
          <div v-if="!blogs" class="nof">
            No feeds follow some users to see their Blogs.
          </div>
        </div>
        <!-- {% block innercontent %} {% endblock %} -->
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "HomeView",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      // fullname: null,
      // email: null,
      auth_token: null,
      users: null,
      error: "",
      sucess: "",
      blogs: null,
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.username = sessionStorage.getItem("username");
    console.log(this.username);
    if (!this.auth_token) {
      alert("Please Login to see your dashboard.");
      this.$router.push("/");
    }
    return fetch("http://127.0.0.1:5000/api/user", {
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
        this.blogs = data["blogs"];
        console.log(data["blogs"]);
        console.log(this.blogs);
        console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
  methods: {
    async usr(user) {
      this.$router.push(`/profile/${user}`);
    },
    async comment(bgid) {
      this.$router.push(`/comment/${bgid}`);
    },
    async readblog(bgid) {
      this.$router.push(`/readblog/${bgid}`);
    },
    async like(blog) {
      const res = await fetch(`http://127.0.0.1:5000/api/likeunlike`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${this.auth_token}`,
        },
        body: JSON.stringify({
          like: true,
          blog: blog,
          username: this.currusername,
          is_authenticated: true,
        }),
      });
      if (res.ok) {
        console.log("liked");
        this.$router.go();
        window.location.reload();
      } else {
        console.log("error!!");
      }
    },
    async unlike(blog) {
      const res = await fetch(`http://127.0.0.1:5000/api/likeunlike`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${this.auth_token}`,
        },
        body: JSON.stringify({
          like: false,
          blog: blog,
          username: this.currusername,
          is_authenticated: true,
        }),
      });
      if (res.ok) {
        this.$router.go();
        window.location.reload();
        console.log("unliked");
      } else {
        console.log("error!!");
      }
    },
  },
};
</script>

<style>
/* @import url("https://fonts.googleapis.com/css2?family=Rubik+Pixels&display=swap"); */
/* @import url("https://fonts.googleapis.com/css2?family=Righteous&display=swap"); */
@import url("https://fonts.googleapis.com/css2?family=Rubik+Gemstones&display=swap");
.content-area {
  background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),
    url("../assets/s2.png") no-repeat center/cover;
  display: flex;
  border: 1px solid blue;
  min-height: 91vh;
  position: relative;
  overflow: auto;
}

.content {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  width: 90%;
  margin: 30px auto 30px;
  align-items: center;
  position: relative;
  min-height: 75vh;
}

.head-nav {
  position: absolute;
  top: -24px;
  width: 100%;
  height: 80px;
  /* margin: 20px; */
  /* margin: 10px; */
  /* overflow: hidden; */
  display: inline-block;
  /* border: 1px solid gold; */
}
.head-nav a {
  height: 50px;
  font-size: 2rem;
  /* font-weight: bold; */
  font-family: "Rubik Gemstones", cursive;
  /* font-family: "Rubik Pixels", cursive; */
  /* font-family: "Righteous", cursive; */
  margin: 15px;
  padding: 10px;
  color: rgb(255, 255, 255);
  display: inline-block;
  text-decoration: none;
  /* border: 2px solid black; */
  box-shadow: 2px 2px 4px 4px gray;
  /* background: rgb(233, 233, 233); */
  background: transparent;
  cursor: pointer;
  /* float: left; */
}
.head-nav a:hover {
  /* background: wheat; */
  box-shadow: 3px 3px 5px 5px rgb(255, 233, 137);
  transition: 0.5s;
}
/* .rp {
  display: ;
  left: 0px;
} */

.nof {
  text-align: center;
  /* border: 1px solid red; */
  color: #ffffff;
  top: 230px;
  position: absolute;
  width: 800px;
  right: 250px;
  font-family: "Rubik Bubbles", cursive;
  font-size: 2rem;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #00ebfc;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5));
}
.allposts {
  /* background: url("../static/pp12.jpg") no-repeat center/cover; */
  background: transparent;
  position: absolute;
  top: 44px;
  width: 97%;
  min-height: 700px;
}

.posts {
  /* left: 20px; */
  /* position: relative; */
  overflow: hidden;
  display: flex;
  flex-direction: row;
  margin: 30px 0;
  width: 100%;
  max-height: 270px;
  border-radius: 0px;
  background: white;
  /* border: 1px solid red; */
  box-shadow: 5px 5px 15px 6px #8706ff;
}

.posts:hover {
  box-shadow: 0px 5px 15px 6px rgb(255, 233, 143);
}

.posts img {
  width: 40%;
  height: 270px;
  float: left;
  margin: 0%;
  /* border: 1px solid yellowgreen; */
}

.post-preview {
  width: 60%;
  padding: 0px;
  float: right;
  margin-left: 5px;
  /* border: 1px solid red; */
  position: relative;
  height: 270px;
}
.post-preview h1 {
  /* border: 1px solid red; */
  display: absolute;
  top: 0px;
  max-height: 80px;
  overflow: hidden;
  margin: 0px;
  text-align: left;
}
.preview-text {
  position: absolute;
  /* border: 1px solid red; */
  top: 100px;
  max-height: 100px;
  max-width: 870px;
  overflow: hidden;
}
.intr {
  position: absolute;
  font-size: 1.7rem;
  bottom: 0px;
}
.intr a {
  color: gray;
  margin-left: 4px;
}
/* #lk {
  color: red;
} */
.cmnt {
  color: gray;
  cursor: pointer;
}
.lk {
  color: gray;
}
.lk:hover {
  color: red;
  cursor: pointer;
}

.cmnt:hover {
  color: rgb(63, 62, 62);
}
#usr {
  color: blue;
  font-weight: bold;
}
#usr:hover {
  color: rgb(72, 17, 201);
  cursor: pointer;
}

.btn {
  padding: 0.5rem 1rem;

  background: transparent;
  color: rgb(116, 20, 196);
  border: 1px solid transparent;
  border-radius: 0.25rem;
  text-decoration: none;
  cursor: pointer;
  position: absolute;
  right: 7px;
  bottom: 7px;
  font-weight: 600;
  font-size: 1.15rem;
  box-shadow: 1.2px 1.2px 1.2px 1.2px grey;
}

.btn:hover {
  /* background: #4a1e85; */
  background: #6939a7;
  box-shadow: 2px 2px 1.8px 2px rgb(80, 79, 79);
  transition: 0.5s;
  color: white;
}
</style>

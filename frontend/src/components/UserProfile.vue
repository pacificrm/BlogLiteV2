<template>
  <div class="above">
    <NavBar :username="this.currusername"></NavBar>
    <div class="all">
      <div class="profile">
        <div class="profilePic">
          <img :src="require(`@/assets/profile/${profile_pic}`)" alt="" />
        </div>
        <div class="pid">{{ this.username }}</div>
        <div class="pname">{{ this.fullname }}</div>
        <div class="pabout">{{ this.about }}</div>

        <div class="data">
          <a href="#"
            ><span> Total posts <br />{{ this.totalpost }}</span>
          </a>

          <a href="/followers"
            ><span> Followers <br />{{ this.followers }}</span></a
          >
          <a href="/followings"
            ><span>
              Following <br />
              {{ this.following }}</span
            ></a
          >
        </div>
        <div
          v-if="currusername === username"
          class="edit"
          id="ex"
          @click="exporting()"
        >
          <a href="#" id="ett">Export</a>
        </div>
        <div v-if="currusername === username" class="edit">
          <a href="/editprofile" id="et">Edit</a>
        </div>
      </div>
      <div class="myposts">
        <div v-for="blog of blogs" :key="blog.id" class="posts">
          <img
            :src="require(`@/assets/blogs/${blog.image}`)"
            alt="Post Image"
            class="post-image"
          />
          <div class="post-preview">
            <h1>
              <!-- {{ blog["title"] }} -->
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
                >{{ blog["date"] }}&nbsp;&nbsp;{{ blog["time"] }}
              </i>
            </div>
            <p class="preview-text">
              <span v-html="blog['preview']"></span>
              <!-- {{ blog["preview"] }} -->
            </p>
            <div class="intr">
              {{ blog["likes"] }}
              <i class="fa fa-thumbs-up lk" @click="like(blog['id'])"> </i>
              &nbsp;&nbsp; {{ blog["dislikes"] }}
              <i class="fa fa-thumbs-down lk" @click="unlike(blog['id'])"> </i>
              &nbsp;&nbsp; {{ blog["comments"] }}
              <i @click="comment(blog['id'])" class="fa fa-comment cmnt"></i>
              &nbsp;&nbsp;
              <i
                v-if="currusername === username"
                class="fa fa-pen cmnt"
                @click="editblog(blog['id'])"
              >
              </i
              >&nbsp;&nbsp;
              <i
                v-if="currusername === username"
                class="fa fa-trash lk"
                @click="del(blog['id'])"
              >
              </i>
            </div>

            <a href="#" class="btn" @click.prevent="readblog(blog['id'])"
              >Read More</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";
// import sanitizeHtml from "sanitize-html";

export default {
  name: "UserProfile",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      currusername: null,
      about: null,
      email: null,
      auth_token: null,
      followers: 0,
      following: 0,
      totalpost: 0,
      blogs: null,
      profile_pic: "no-profile-pic.jpeg",
      error: "",
      good: "",
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.currusername = sessionStorage.getItem("username");
    this.username = this.$route.params.username;
    // console.log(username);
    // console.log(this.email)
    // if (!this.auth_token) {
    //   alert("Please Login to see your dashboard.");
    //   this.$router.push("/");
    // }
    return fetch(`http://127.0.0.1:5000/api/profile/${this.username}`, {
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
        this.email = data["email"];
        this.fullname = data["fullname"];
        this.about = data["about"];
        this.followers = data["followers"];
        this.following = data["following"];
        this.totalpost = data["totalpost"];
        this.profile_pic = data["profile_pic"];
        this.blogs = data["blogs"];
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
    async editblog(bgid) {
      this.$router.push(`/editblog/${bgid}`);
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
      // this.success = null;
      // this.error = null;
      window.location.reload();
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
        console.log("unliked");
        this.$router.go();
        window.location.reload();
      } else {
        console.log("error!!");
      }
    },
    async del(id) {
      // var txt;
      if (confirm("Want to delete this Blog !!")) {
        const res = await fetch(`http://127.0.0.1:5000/api/blog/${id}`, {
          method: "DELETE",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authentication-Token": `${this.auth_token}`,
          },
          // body: JSON.stringify({
          //   user: this.username,
          //   cmnt: this.cmnt,
          //   is_authenticated: true,
          // }),
        });
        if (res.ok) {
          this.$router.go();
          window.location.reload();
          console.log("commentd");
          // this.success = "Followed.";
        } else if (res.status === 400) {
          console.log("error!!");
        }
        console.log("You pressed OK!");
      } else {
        console.log("You pressed Cancel!");
        this.$router.go();
        window.location.reload();
      }
    },
    async exporting() {
      const res = await fetch(`http://127.0.0.1:5000/api/exportblogs`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${this.auth_token}`,
        },
      });
      if (res.ok) {
        alert("Blogs exported");
        // this.$router.go();
        // window.location.reload();
        console.log("exported");
      } else {
        alert(" NO Blogs to export");
        console.log("error!!");
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Handlee&family=Rubik+Gemstones&family=Rubik+Spray+Paint&display=swap");
.profile {
  position: relative;
  min-height: 30vh;
  border: 1px solid red;
  margin: 0px;
  height: 250px;
  background: url("../assets/back.jpg") no-repeat center/cover;
}

/* .all {
  max-height: 500px;
  overflow: auto;
} */

.profilePic {
  width: 180px;
  height: 180px;
  border: 1px solid blue;
  margin: 30px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.profilePic img {
  width: 100%;
  height: 100%;
}

.pid {
  border: 0px solid white;
  position: absolute;
  left: 240px;
  top: 75px;
  color: white;
  font-family: "Rubik Gemstones", cursive;

  padding: 5px;
  height: 37px;
  width: 220px;
  text-align: center;
  font-size: 2rem;
}

.pname {
  border: 0px solid white;
  position: absolute;
  left: 240px;
  font-family: "Rubik Gemstones", cursive;
  top: 125px;
  color: white;
  padding: 5px;
  height: 65px;
  width: 220px;
  text-align: center;
  font-size: 1.8rem;
  overflow: hidden;
}
.pabout {
  /* border: 1px solid white; */
  position: absolute;
  left: 257px;
  font-family: "Handlee", cursive;
  /* top: 140px; */
  bottom: 7px;
  color: white;
  padding: 5px;
  height: 40px;
  width: 850px;
  text-align: left;
  font-size: 1.5rem;
  overflow: hidden;
}
.data {
  font-family: "Rubik Spray Paint", cursive;
  display: inline-block;
  position: absolute;
  /* border: 1px solid red; */
  top: 90px;
  right: 120px;
  width: 800px;
  overflow: hidden;
}
.data span {
  display: inline-block;
  color: rgb(212, 212, 212);
  /* border: 1px solid white; */
  border: transparent;
  font-size: 2.5em;
  padding: 2px;
  text-align: center;
  margin: 10px 20px;
}

.data span:hover {
  color: white;
  /* text-shadow: 1px 1px gray; */
}
/* .data span:nth-child(1):hover {
  box-shadow: 2px 2px 4px #f5f5f5;
  font-size: 1.6rem;
}
.data span:nth-child(2):hover {
  box-shadow: 2px 2px 4px #f5f5f5;
  font-size: 1.6rem;
}
.data span:nth-child(3):hover {
  box-shadow: 2px 2px 4px #f5f5f5;
  font-size: 1.6rem;
} */
.edit {
  position: absolute;
  right: 10px;
  bottom: 0px;
  padding: 10px;
  /* display: inline-block; */
  /* box-shadow: 5px, 5px, 5px, 5px rgb(240, 238, 241); */
  /* color: rgb(231, 27, 221); */

  /* border: 1px solid green; */
}
/* .edit:hover {
  background: #ec09ec;
} */

#ex {
  position: absolute;
  top: 0px;
  right: 0px;
}

#ett {
  background-color: aliceblue;
}

#ex {
  font-size: 2rem;
}
#et {
  font-size: 2rem;
  background-color: aliceblue;
}
.edit a {
  border: 5px solid rgb(48, 49, 2);
  display: inline-block;
  color: #062bfc;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #0c6ff0;
  font-size: 2rem;
  text-decoration: none;
  /* box-shadow: 5px, 5px, 5px, 5px rgb(240, 238, 241); */
  font-weight: bold;
  font-family: "Handlee", cursive;
}
.edit a:hover {
  color: #9fff06;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #051f1b;
}
/* .allposts {
 
  background: transparent;
  position: absolute;
  top: 80px;
  width: 97%;
  min-height: 700px;
} */

.myposts {
  /* position: absolute; */
  border: 2px solid red;
  min-height: 433px;
  overflow: "auto";
  position: absolute;
  width: 1520px;
  background: linear-gradient(rgba(45, 3, 80, 0.6), rgba(4, 12, 56, 0.6)),
    url("../assets/9.jpg") no-repeat center/cover;
}
.posts {
  left: 25px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: row;
  margin: 30px 0;
  width: 96%;
  max-height: 270px;
  border-radius: 0px;
  background: white;
  /* border: 1px solid red; */
  box-shadow: 5px 5px 15px #8706ff;
}

.posts:hover {
  box-shadow: 0px 5px 15px brown;
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
  text-align: left;
  max-height: 79px;
  overflow: hidden;
  margin: 0px;
  text-overflow: ellipsis;
}
.preview-text {
  position: absolute;
  /* border: 1px solid red; */
  top: 100px;
  max-height: 94px;
  max-width: 870px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.intr {
  /* border: 1px solid blue; */
  /* color: #6939a7; */
  position: absolute;
  font-size: 1.7rem;
  bottom: 0px;
}
/* .intr a {
 
  color: gray;
  margin-left: 4px;
} */
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

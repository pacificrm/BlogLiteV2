<template>
  <div class="all">
    <NavBar :username="this.username"></NavBar>
    <div class="postBlog">
      <form
        action="http://127.0.0.1:8080/postblog"
        enctype="multipart/form-data"
        method="POST"
      >
        <div class="pp">
          <label for="blogTitle" maxlength="80"> Blog Title</label>
          <!-- <input id="pt" type="textarea" name="postTitle" required /> -->
          <textarea
            v-model="this.Blogdata.blogTitle"
            id="pt"
            cols="500"
            rows="1"
            required
          ></textarea>
        </div>
        <div class="pp">
          <label for="blogPreview"> Blog preview </label>
          <!-- <input id="ppp" type="textarea" name="postPreview" required /> -->
          <textarea
            v-model="this.Blogdata.blogPrev"
            id="ppp"
            cols="500"
            rows="4"
            required
          ></textarea>
        </div>
        <div class="pp">
          <label for="blogContent"> Write Your Blog </label>
          <!-- <input id="pc" type="textarea" name="postContent" required /> -->
          <textarea
            v-model="Blogdata.blogContent"
            cols="56"
            id="pc"
            rows="10"
            required
          ></textarea>
        </div>
        <div class="pp">
          <input ref="fileinput" id="pi" type="file" @input="uploadImage()" />
        </div>
        <div class="pp">
          <input
            id="pb"
            type="submit"
            value="Update"
            @click.prevent="postBlog()"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "EditBlog",
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
  methods: {
    async uploadImage() {
      let img = this.$refs.fileinput.files;
      this.Blogdata.blogImage = img[0];
      console.log(img[0]);
      // console.log();
      // console.log(event.target.files[0]);
      // this.Blogdata.blogImage = event.target.files[0];
    },

    async postBlog() {
      console.log(this.Blogdata.blogContent);
      let formData = new FormData();
      formData.append("blogImage", this.Blogdata.blogImage);
      formData.append("blogTitle", this.Blogdata.blogTitle);
      formData.append("blogPrev", this.Blogdata.blogPrev);
      formData.append("blogContent", this.Blogdata.blogContent);
      console.log(formData);
      console.log(sessionStorage.getItem("auth-token"));
      for (var key of formData.entries()) {
        console.log(key[0], key[1]);
      }
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/blog/${this.bgid}`, {
          mode: "cors",
          method: "PuT",
          headers: {
            "Access-Control-Allow-Origin": "*",
            // "Content-Type": "multipart/form-data",
            "Authentication-Token": sessionStorage.getItem("auth-token"),
          },
          body: formData,
        });
        if (res.ok) {
          console.log("Blog-Posted");
          this.$router.push(`/profile/${this.username}`);
        }
      } catch (error) {
        console.log("Cannot post ", error);
      }
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Rubik+Bubbles&display=swap");
.postBlog {
  top: 56px;
  /* left: 20px; */
  font-family: "Rubik Bubbles", "cursive";
  color: rgb(221, 245, 9);
  position: absolute;
  width: 96vw;
  height: 621px;
  /* left: 10%; */
  margin-top: 10px;
  background: linear-gradient(rgba(45, 3, 80, 0.6), rgba(4, 12, 56, 0.6)),
    url("../assets/pb3.jpg") no-repeat center/cover;
  border: 1px solid red;
  padding: 30px;
  font-size: 1.7rem;
}
.postBlog label {
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #9c077c;
  /* font-weight: bold; */
}

/* .postBlog input {
    height: 30px;
    margin: 10px;
    width: 200px;
  } */
form {
  margin: 0px;
  padding: 0px;
}
.pp {
  /* border: 1px solid green; */
  display: flex;
  flex-direction: row;
  margin: 10px 20px 10px;
  position: relative;
  min-height: 35px;
}
/* .pp label {
    font-size: 2rem;
  } */
.pp input {
  margin-left: 10px;
  font-size: 1.8rem;
  font-family: "Rubik Bubbles", "cursive";
}
.pp textarea {
  font-size: 1.5rem;
  margin-left: 10px;
  resize: none;
  color: rgb(223, 236, 240);
  background: transparent;
  box-shadow: 2px 2px 2px 4px rgb(39, 3, 59);
}
#pt {
  font-size: 2rem;
  width: 1200px;
  margin-left: 93px;
  margin-bottom: 20px;
  font-weight: bold;
}

#ppp {
  font-size: 1.2rem;
  width: 1201px;
  margin-left: 43px;
  margin-bottom: 20px;
  font-weight: bold;
}

#pc {
  width: 1199px;
  font-size: 1.2rem;
  margin-bottom: 20px;
  font-weight: bold;
}

#pi {
  position: absolute;
  left: 620px;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #9c077c;
}

#pb {
  margin-top: 8px;
  position: absolute;
  left: 680px;
  cursor: pointer;
  font-size: 2rem;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: #9c077c;
}

#pb:hover {
  background: rgb(53, 52, 52);
  color: white;
  box-shadow: 4px 4px 8px rgb(228, 153, 5);
}
</style>

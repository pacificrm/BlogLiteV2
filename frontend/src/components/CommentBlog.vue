<template>
  <div class="cm">
    <NavBar :username="this.username"></NavBar>
    <div class="comments">
      <a class="bck" href="/home"> Back </a>

      <div class="inputarea">
        <form method="POST">
          <textarea v-model="this.cmnt" cols="75" rows="4"></textarea>
          <input type="submit" value="Comment" @click.prevent="comment()" />
          <!-- <i class="fa fa-paper-plane"></i> -->
        </form>
      </div>
      <div class="showarea">
        <span class="ut">
          <!-- {% if cmnts %}
          {% for cmnt in cmnts %} -->
          <div v-for="cmnt of comments" :key="cmnt.id" class="coment">
            <span id="inf"
              ><i class="far fa-user"> </i> {{ cmnt["username"] }}
              {{ cmnt["date"] }} {{ cmnt["time"] }}</span
            >
            <!-- {% if cmnt['user_name'] == current_user.user_name %} -->
            <a style="color: aliceblue" href="#">
              <i
                v-if="cmnt['username'] === username"
                style="float: right"
                class="fa fa-trash"
                @click="del(cmnt['id'])"
              ></i>
            </a>
            <br />
            <span style="font-size: 2rem" v-html="cmnt['comment']"></span>
          </div>
        </span>
      </div>
      <!-- {% endfor %} 
        {% endif %}     -->
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "CommmentBlog",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      blogid: null,
      comments: null,
      cmnt: null,
      auth_token: null,
      error: "",
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.username = sessionStorage.getItem("username");
    this.blogid = this.$route.params.id;
    console.log(this.blogid);
    if (!this.auth_token) {
      alert("Please Login to see your dashboard.");
      this.$router.push("/");
    }
    return fetch(`http://127.0.0.1:5000/api/comment/${this.blogid}`, {
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
        this.comments = data["comments"];
        // console.log(data["blogs"]);
        // console.log(this.comments);
        // console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
  methods: {
    async comment() {
      const res = await fetch(
        `http://127.0.0.1:5000/api/comment/${this.blogid}`,
        {
          method: "POST",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authentication-Token": `${this.auth_token}`,
          },
          body: JSON.stringify({
            user: this.username,
            cmnt: this.cmnt,
            is_authenticated: true,
          }),
        }
      );
      if (res.ok) {
        this.$router.go();
        window.location.reload();
        console.log("commentd");
        // this.success = "Followed.";
      } else if (res.status === 400) {
        console.log("error!!");
      }
    },
    async del(id) {
      // var txt;
      if (confirm("Want to delete this comment !!")) {
        const res = await fetch(`http://127.0.0.1:5000/api/comment/${id}`, {
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
  },
};
</script>

<style scoped>
.comments {
  /* border: 1px solid red; */
  min-height: 91vh;
  margin: 0px;
  position: relative;
  background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
    url("../assets/s3.png") no-repeat center/cover;
}

.bck {
  text-decoration: none;
  display: block;
  color: azure;
  position: absolute;
  right: 10px;
  top: 10px;
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
.inputarea {
  /* border: 1px solid blue; */
  top: 10px;
  position: absolute;
  left: 420px;
  width: 700px;
  text-align: center;
  font-size: 1.5rem;
  overflow: hidden;
}
.inputarea textarea {
  color: white;
  background: transparent;
  resize: none;
  font-size: 1.5rem;
  font-weight: 800;
  width: 99%;
  margin: 0px;
  font-family: "Indie Flower", cursive;
  box-shadow: 0px 5px 15px gainsboro;
}
.inputarea input {
  font-size: 1.4rem;
  border-radius: 20px;
  font-family: "Rubik Spray Paint", cursive;
  padding: 8px;
  background: gainsboro;
}
.inputarea input:hover {
  background: #5ce7ff;
  color: #383737;
}

.showarea {
  /* border: 1px solid red; */
  width: 700px;
  left: 420px;
  top: 230px;
  position: absolute;
  min-height: 60vh;
  max-height: 60vh;
  overflow: auto;
  margin-bottom: 0px;
  padding-bottom: 0px;
}

.coment {
  position: relative;
  text-align: left;
  width: 675px;
  /* border: 1px solid red; */
  color: aliceblue;
  font-size: 1.5rem;
  font-weight: 900;
  font-family: "Indie Flower", cursive;
  margin: 20px 0px;
  padding: 10px;
}

.fa-trash {
  color: bisque;
}
.fa-trash:hover {
  color: red;
  cursor: pointer;
}

#inf {
  float: left;
  font-size: 1.2rem;
  color: bisque;
}
</style>

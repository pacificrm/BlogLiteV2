<template>
  <div class="editp">
    <NavBar :username="this.username"></NavBar>
    <div class="editprofile">
      <div class="pform">
        <form
          action="http://127.0.0.1:8080/editprofile"
          method="POST"
          enctype="multipart/form-data"
        >
          <label for="fullname">Name :</label>
          <input
            type="text"
            v-model="this.fullname"
            placeholder="Enter your full name"
            required
          />
          <br />
          <label for="about">About :</label>
          <input
            type="text"
            v-model="this.about"
            placeholder="Enter about yourself"
            required
          />
          <br />
          <label for="email">Email :</label>
          <input
            style="color: black"
            type="email"
            v-model="this.email"
            disabled
          />
          <br />
          <label for="Username">Username :</label>
          <input
            type="text"
            style="color: black"
            v-model="this.username"
            disabled
          />
          <br />
          <label for="profilepic">Profile-Pic :</label>
          <input
            style="color: wheat"
            type="file"
            ref="fileinput"
            @input="uploadImage()"
          />
          <br />
          <input
            type="submit"
            id="btn"
            value="update"
            @click.prevent="updateprofile()"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "EditProfile",
  components: {
    NavBar,
  },
  data() {
    return {
      username: null,
      about: null,
      email: null,
      auth_token: null,
      // lists: {},
      profile_pic: null,
      error: "",
      good: "",
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
        this.email = data["email"];
        this.fullname = data["fullname"];
        this.about = data["about"];
        console.log(data);
      })
      .catch((error) => console.log("1st", error));
  },
  methods: {
    async uploadImage() {
      let img = this.$refs.fileinput.files;
      this.profile_pic = img[0];
      console.log(img[0]);
    },

    async updateprofile() {
      let formData = new FormData();
      formData.append("fullname", this.fullname);
      formData.append("about", this.about);
      formData.append("profile_pic", this.profile_pic);
      console.log(formData);
      console.log(sessionStorage.getItem("auth-token"));
      // for (var key of formData.entries()) {
      //   console.log(key[0], key[1]);
      // }
      try {
        const res = await fetch("http://127.0.0.1:5000/api/user", {
          mode: "cors",
          method: "PUT",
          headers: {
            "Access-Control-Allow-Origin": "*",
            // "Content-Type": "multipart/form-data",
            "Authentication-Token": sessionStorage.getItem("auth-token"),
          },
          body: formData,
        });
        if (res.ok) {
          console.log("Profile-Updated");
          this.$router.push(`profile/${this.username}`);
        }
      } catch (error) {
        console.log("Cannot Update ", error);
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Yeon+Sung&display=swap");
.editp {
  /* border: 1px solid red; */
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("../assets/s3.png") no-repeat center/cover;
}
.editprofile {
  /* border: 1px solid red; */
  min-height: 78vh;
  margin: 55px 200px 29px;
  position: relative;
  font-size: 1.5rem;
  background: transparent;
  /* background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url("../assets/pp14.jpeg") no-repeat center/cover; */
  /* text-align: center; */
}
.pform {
  /* border: 1px solid red; */
  position: absolute;
  width: 70%;
  left: 160px;
  margin: 0px;
  height: 100%;
}
.editprofile form {
  /* border: 1px solid green; */
  position: relative;
  height: 100%;
  width: 100%;
}
.editprofile label {
  color: wheat;
  margin: 40px;
}
.editprofile input {
  /* border: 1px solid blue; */
  padding: 10px;
  font-size: 1.5rem;
  margin: 20px;
  width: 500px;
  font-family: "Yeon Sung", cursive;
  /* text-align: center; */
}

#btn {
  text-transform: uppercase;
  position: absolute;
  bottom: 5px;
  margin: 10px;
  width: 140px;
  border-radius: 60px;
  left: 320px;
  font-weight: 900;
}
#btn:hover {
  /* background: #4a1e85; */
  background: #6939a7;
  box-shadow: 2px 2px 1.8px 2px rgb(80, 79, 79);
  transition: 0.5s;
  color: white;
  cursor: pointer;
}
</style>

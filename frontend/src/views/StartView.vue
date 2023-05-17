<template>
  <div class="start">
    <!-- <h1>This is an about page</h1> -->
    <!-- <StartPage /> -->
    <StartPage v-show="t" />
    <LoginSignup
      v-show="!t"
      @signup="(signupData = $event), register()"
      @login="(loginData = $event), login()"
      :serror_1="signupData.error_1"
      :serror_2="signupData.error_2"
      :lerror_1="loginData.error_1"
      :lerror_2="loginData.error_2"
      :success="signupData.success"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import StartPage from "@/components/StartPage.vue";
import LoginSignup from "@/components/LoginSignup.vue";
// import StartPage from "@/components/StartPage.vue";
// import { clearInterval } from "timers";

export default {
  name: "StartView",
  components: {
    StartPage,
    LoginSignup,
  },

  data() {
    return {
      t: true,
      signupData: {
        email: null,
        username: null,
        password1: null,
        password2: null,
        error_1: "",
        error_2: "",
        success: "",
      },
      loginData: {
        username: null,
        password: null,
        error_1: "",
        error_2: "",
        auth: null,
        is_authenticated: false,
      },
    };
  },
  async created() {
    setTimeout(() => (this.t = false), 7000);

    sessionStorage.clear();
    localStorage.clear();
  },
  // async created() {

  // },
  async updated() {
    sessionStorage.clear();
    localStorage.clear();
  },
  methods: {
    async register() {
      console.log(this.signupData);
      this.signupData.error_1 = null;
      this.signupData.error_2 = null;
      this.signupData.success = null;
      if (
        this.emailValidation(this.signupData.email) &&
        this.passValidation(this.signupData.password1) &&
        this.passConfirmation(
          this.signupData.password1,
          this.signupData.password2
        )
      ) {
        try {
          const res = await fetch("http://127.0.0.1:5000/api/user", {
            mode: "cors",
            method: "POST",
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.signupData.email,
              username: this.signupData.username,
              password1: this.signupData.password1,
            }),
          });
          // .then((response) => response.json())
          // .then(async (data) => {
          //   console.log(data);
          //   this.$router.go(-1);
          //   this.signupData.success =
          //     "Signedup succesfully!! login to continue.";
          //   // alert("Signedup succesfully!! login to continue.");
          // })
          // .catch((err) => {
          //   console.log(err);
          //   this.signupData.success = "";
          //   this.signupData.error_1 = "User already exists!! Try again.";
          // });

          if (res.ok) {
            console.log("registered");
            this.signupData.success =
              "Signedup succesfully!! login to continue.";
          } else if (res.status === 400) {
            this.signupData.error_1 = "Email  already exists!! Try again.";
          } else if (res.status === 401) {
            this.signupData.error_1 = "Username already exists!! Try again.";
          } else {
            this.signupData.error_1 = "Registration Failed!! Try again.";
            throw new Error("Registration failed");
          }
        } catch (error) {
          console.log("Registration Failed: ", error);
        }
      } else if (!this.emailValidation(this.signupData.email)) {
        this.signupData.error_1 = "Please enter a valid email";
      } else if (!this.passValidation(this.signupData.password1)) {
        this.signupData.error_1 = "Password requires atleast 8 characters.";
      } else if ((this.signupData.password1, this.signupData.password2)) {
        this.signupData.error_1 = "Password didn't matched!!";
      }
    },
    emailValidation: function (email) {
      var result =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
      return result.test(email);
    },
    passValidation: function (passs) {
      var result = /.{8,}/;
      return result.test(passs);
    },
    passConfirmation: function (passs1, passs2) {
      if (passs1 == passs2) {
        return true;
      }
      return false;
    },
    async login() {
      this.loginData.error_2 = null;
      this.loginData.error_1 = null;
      try {
        fetch("http://127.0.0.1:5000/login?include_auth_token", {
          mode: "cors",
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.loginData.username,
            password: this.loginData.password,
            is_authenticated: true,
          }),
        })
          .then((resp) => resp.json())
          .then(async (data) => {
            const { response } = data;
            console.log(data);
            if (response.errors) {
              if (response.errors[1]) {
                this.loginData.error_1 = response.errors[1];
              }
              this.loginData.error_2 = response.errors[0];
              console.log(this.loginData.error_1, this.loginData.error_2);
            } else {
              this.loginData.auth = response.user.authentication_token;
              sessionStorage.setItem("auth-token", this.loginData.auth);
              sessionStorage.setItem("username", this.loginData.username);
              this.$router.push("home");
              console.log("its homepage");
            }
          })
          .catch((error) => {
            console.log("some error occured", error);
          });
      } catch (error) {
        console.log("No way!! ", error);
      }
    },
  },
};
</script>

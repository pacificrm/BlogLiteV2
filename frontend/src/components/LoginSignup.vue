<template>
  <div class="bd">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css"
    />
    <div id="popup">
      <p class="alert alert-danger alert-dismissible fade show" v-if="serror_1">
        {{ serror_1
        }}<button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </p>
      <p class="alert alert-danger alert-dismissible fade show" v-if="serror_2">
        {{ serror_2
        }}<button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </p>
      <p class="alert alert-danger alert-dismissible fade show" v-if="lerror_1">
        {{ lerror_1
        }}<button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </p>
      <p class="alert alert-danger alert-dismissible fade show" v-if="lerror_2">
        {{ lerror_2
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
      <!-- {% with messages=get_flashed_messages(with_categories=true) %} {% if
      messages %} {% for category, message in messages%}
      <div
        class="alert alert-{{ category }} alert-dismissible fade show"
        role="alert"
      >
        {{ message }}
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
      {% endfor %} {% endif %} {% endwith %} -->
    </div>

    <div id="main">
      <input class="out" type="checkbox" id="ck" aria-hidden="true" />

      <!--                         SIGNUP PAGE                    -->

      <div class="signup">
        <form ref="sigform" method="Post">
          <label class="lb" for="ck" aria-hidden="true">Sign up</label>
          <input
            class="out"
            type="text"
            v-model="signupData.username"
            placeholder="Enter User Name*"
            required
          />
          <input
            class="out"
            type="email"
            v-model="signupData.email"
            placeholder="Enter Email Id*"
            required
          />
          <input
            class="out"
            type="password"
            v-model="signupData.password1"
            placeholder="Enter Password*"
            required
          />
          <input
            class="out"
            type="password"
            v-model="signupData.password2"
            placeholder="Confirm Password*"
            required
          />
          <button
            type="submit"
            class="tk"
            @click.prevent="
              $emit('signup', signupData);
              resetForm();
            "
          >
            Sign up
          </button>
        </form>
      </div>

      <!--                         LOGIN PAGE                            -->

      <div class="login">
        <form method="Post">
          <label class="lb" for="ck" aria-hidden="true">Login</label>
          <input
            class="out"
            type="text"
            v-model="loginData.username"
            placeholder="Enter your Username"
            required
          />
          <input
            class="out"
            type="password"
            v-model="loginData.password"
            placeholder="Password"
            required
          />
          <button
            type="submit"
            class="tk"
            @click.prevent="$emit('login', loginData)"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginSignup",
  data() {
    return {
      signupData: {
        email: null,
        username: null,
        password1: null,
        password2: null,
        error_1: "",
        error_2: "",
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
  props: {
    serror_1: {
      default: "",
    },
    serror_2: {
      default: "",
    },
    lerror_1: {
      default: "",
    },
    lerror_2: {
      default: "",
    },
    success: {
      default: "",
    },
  },

  async created() {
    sessionStorage.clear();
    localStorage.clear();
  },
  async updated() {
    sessionStorage.clear();
    localStorage.clear();
  },
  methods: {
    resetForm() {
      this.$refs.sigform.reset();
      this.signupData.email = null;
      this.signupData.username = null;
      this.signupData.password1 = null;
      this.signupData.password2 = null;
    },
  },
};
</script>
<!-- <script
  src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8"
  crossorigin="anonymous"
></script> -->

<style scoped>
.bd {
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: "jost", sans-serif;
  background: url("../assets/2.jpg") no-repeat center/cover;
}
#main {
  width: 350px;
  height: 550px;
  background: red;
  overflow: hidden;
  background: url("../assets/1.jpg") no-repeat center / cover;
  border-radius: 10px;
  box-shadow: 5px 20px 50px #000;
}
#ck {
  display: none;
}
.signup {
  position: relative;
  width: 100%;
  height: 100%;
}

.lb {
  color: #fff;
  font-size: 2.3em;
  justify-content: center;
  display: flex;
  margin: 60px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.5s ease-in-out;
}

.out {
  width: 75%;
  height: 35px;
  background: #e0dede;
  justify-content: center;
  display: flex;
  margin: 20px auto;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 5px;
}

.tk {
  width: 60%;
  height: 40px;
  margin: 10px auto;
  background: #e0dede;
  justify-content: center;
  display: block;
  color: #fff;
  background: #573b8a;
  font-size: 1em;
  font-weight: bold;
  margin-top: 20px;
  outline: none;
  border: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}

.tk:hover {
  background: #6d44b8;
}

.login {
  height: 500px;
  background: #eee;
  border-radius: 60% / 10%;
  transform: translateY(-180px);
  transition: 0.8s ease-in-out;
}

.login label {
  color: #573b8a;
  transform: scale(0.6);
}

#ck:checked ~ .login {
  transform: translateY(-550px);
}

#ck:checked ~ .login label {
  transform: scale(1);
}
#ck:checked ~ .signup label {
  transform: scale(0.6);
}
.login button {
  bottom: 10%;
}

/* p {
  color: red;
} */

input[type="email"]::placeholder,
input[type="password"]::placeholder,
input[type="text"]::placeholder {
  color: #b5a1a1;
}

#popup {
  top: 0px;
  position: absolute;
  width: 500px;
  text-align: center;
}
</style>

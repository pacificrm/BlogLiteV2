<template>
  <div class="st">
    <h2 data-text="&nbsp;BLOGLITE&nbsp;">&nbsp; BLOGLITE &nbsp;</h2>
  </div>
</template>

<script>
export default {
  name: "StartPage",
  //   props: {
  //     msg: String
  //   }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Rubik+Iso&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Rubik Iso", cursive;
}
.st {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #111;
}
h2 {
  position: relative;
  font-size: 8em;
  color: #222;
  -webkit-text-stroke: 1px #050801;
  -webkit-text-stroke-color: #00ebfc;
}

h2::before {
  content: attr(data-text);
  position: absolute;
  color: #03e9f4;
  -webkit-text-stroke: 1px #050801;
  -webkit-text-stroke-color: #00ebfc;
  width: 350px;
  overflow: hidden;
  white-space: nowrap;
  border-right: 4px solid #fff;
  animation: animate 8s linear infinite;
  filter: drop-shadow(0 0 20px #03e9f4);
}

@keyframes animate {
  0%,
  10%,
  100% {
    width: 0;
  }
  70%,
  90% {
    width: 100%;
  }
}
</style>

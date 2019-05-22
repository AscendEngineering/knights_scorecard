var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
  },
  methods: {
      created: function() {
          console.log('Hello World')
      }
  }
});
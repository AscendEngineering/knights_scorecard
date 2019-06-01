var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Time", "# Meetings", "Predicted Income"],
      items: [
        {"Time": "Last year", "# Meetings": "5", "Predicted Income": "$500"},
        {"Time": "Last Month", "# Meetings": "20", "Predicted Income": "$1000"},
      ],
      knights: [
        {"Knight":"Felix"},
        {"Knight":"Konnor"},
        {"Knight":"Jeffrey"},
        {"Knight":"Kaila"},
        {"Knight":"Danica"},
        {"Knight":"Sincere"},
        {"Knight":"Elianna"},
        {"Knight":"Justine"},
        {"Knight":"Paris"},
        {"Knight":"Maria"},
        {"Knight":"Annika"},
        {"Knight":"Dulce"},
        {"Knight":"Axel"},
        {"Knight":"Jaelyn"},
        {"Knight":"Brice"},
        {"Knight":"Leila"},
        {"Knight":"Tamara"},
        {"Knight":"Luke"},
        {"Knight":"Trenton"},
        {"Knight":"Ronnie"},
        {"Knight":"Paula"},
        {"Knight":"Deanna"},
        {"Knight":"Sydney"},
        {"Knight":"Riley"},
        {"Knight":"Houston"},
        {"Knight":"Clarissa"},
        {"Knight":"Aryanna"},
        {"Knight":"Sloane"},
        {"Knight":"Trinity"},
        {"Knight":"Karley"}
      ],

      form: {
        "client_name": "",
        "client_details": "",
        "date": "",
        "time": ""
      }
      
  },
  methods: {
      created: function() {
        console.log('Hello World')
      },
      test: function(){
        console.log("test");
      },
      knight_selected: function(record,indx){
        console.log(indx);
        knight_url = "/knight/" + this.knights[indx]["Knight"];
        window.location.pathname=knight_url;
      },
      new_meeting: function(event){
        event.preventDefault()
        //send axios request
        console.log(this.form.client_name)
        axios.post('',this.form)
          .then(function(response){
            console.log(response);
          })
          .catch(function(response){
            console.log(response)
          });

      }
  }
});
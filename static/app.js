var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Time", "# Meetings", "Predicted Income"],
      items: [
        {"Time": "This Year", "# Meetings": "20", "Predicted Income": "$10000"},
        {"Time": "This Month", "# Meetings": "20", "Predicted Income": "$1000"},
        {"Time": "This Week", "# Meetings": "20", "Predicted Income": "$100"},
        {"Time": "Today", "# Meetings": "1", "Predicted Income": "$50"},
        {"Time": "Last Week", "# Meetings": "2", "Predicted Income": "$100"},
        {"Time": "Last Month", "# Meetings": "20", "Predicted Income": "$1000"},
        {"Time": "Last year", "# Meetings": "120", "Predicted Income": "$10000"}
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
      },
      filter: "",
      currentKnight:""
      
  },
  methods: {
      created: function() {
        console.log('Hello World')
      },
      test: function(){
        console.log("test");
      },
      knight_selected: function(record,indx){
        this.currentKnight = record.Knight
        knight_url = 'knight/?name=' + record.Knight;
        console.log(knight_url)
        window.location.href=knight_url;
      },
      new_meeting: function(event){
        
        //send axios request
        axios.post('',this.form)
          .then(function(response){
          })
          .catch(function(response){
            console.log(response)
          });

          //refresh
          location.reload(false);

      },

      request_metrics: function(days_ago,metrics){
        //create the json with the days ago, metrics, and username
        console.log("TODO");

        //send to the current url

        //on response fill out the html



      }


  }
});
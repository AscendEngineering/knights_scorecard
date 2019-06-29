var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Days", "Past Meetings", "Future Meetings"],
      items: [],
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
      sortBy: "Days",
      currentKnight:""
      
  },
  methods: {
      test: function(){
        console.log("test");
      },
      knight_selected: function(record,indx){
        this.currentKnight = record.Knight;
        knight_url = 'knight/?name=' + record.Knight;
        console.log(knight_url);
        window.location.href=knight_url;
      },
      new_meeting: function(event){
        
        var url = new URL(window.location.href);
        var name = url.searchParams.get("name");
        data_req = this.form;
        data_req["knight"] = name;

        //send axios request
        axios.post('',data_req)
          .then(function(response){
            console.log("sent");
          })
          .catch(function(response){
            console.log(response);
          });

          //refresh
          location.reload(false);

      },

      request_metrics: function(days_ago,metrics){

        //grab username
        var url = new URL(window.location.href);
        var name = url.searchParams.get("name");

        //create the json with the days ago, metrics, and username
        data = {"days_ago": days_ago, "metrics": metrics, "name": name};

        //send to the current url
        axios.get('/metrics',{
          params:data
        })
          .then((response) => {
            this.items.push(response.data);
          })
          .catch(function(response){
            console.log("failed");
          })

      },
  },
  mounted: function() {
    this.request_metrics(1,"");
    this.request_metrics(7,"");
    this.request_metrics(30,"");
    this.request_metrics(365,"");
    

  }
});




var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Days", "Past Meetings", "Future Meetings"],
      items: [],
      knights: [
        {"Knight":"Felix"},
        {"Knight":"Konnor"},
      ],
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
    this.request_metrics(30,"");
  }
});




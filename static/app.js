var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Meeting", "Past Meetings", "Future Meetings"],
      items: [],
      knights: [],
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
 

      request_metrics: function(days_ago,metric){

        //grab username
        var url = new URL(window.location.href);
        var name = url.searchParams.get("name");

        //create the json with the days ago, metrics, and username
        data = {"days_ago": days_ago, "metric": metric, "name": name};

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

      request_knights: function(){
        
        this.knights = [];

        axios.get('/knightList').then((response) => {

          //add knights onto the list
          var knightList = response.data["knights"];
          for(i=0; i<knightList.length;i++){
            this.knights.push({"Knight": knightList[i]});
          }
        })


      }

  },
  mounted: function() {
    if(window.location.href.includes("name")){
      this.request_metrics(30,"Associate");
      this.request_metrics(30,"Insured ");
      this.request_metrics(30,"Postponed");
      this.request_metrics(30,"Cancelled");
      
    }
    else{
      this.request_knights();
    }
    
  }
});




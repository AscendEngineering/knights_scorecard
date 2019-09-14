var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Meeting", "Past Meetings", "Future Meetings"],
      metrics: ["Associate","Insured","Postponed","Cancelled"],
      items: [],
      knights: [],
      filter: "",
      sortBy: "Days",
      currentKnight:"",
      hideLoading: true,
      disableMetricsRequest: false
      
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
 

      request_metrics: function(name,days_ago,metric){

        //create the json with the days ago, metrics, and username
        data = {"days_ago": days_ago, "metric": metric, "name": name};

        //send to the current url
        axios.get('/metrics',{
          params:data
        })
          .then((response) => {
            this.items.push(response.data);

            //hide loading icon
            if(this.items.length == this.metrics.length){
              this.hideLoading = true;
              this.disableMetricsRequest = false;
            }

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


      },

      request_all_metrics: function(event){
        this.items = [];
        this.hideLoading = false;
        this.disableMetricsRequest = true;
        this.metrics.forEach(element => {
          this.request_metrics("all",30,element);
        });
      },

      logout: function(event){
        window.location.href="/logout"
      }

  },
  mounted: function() {
    if(window.location.href.includes("name")){
      
      //grab username
      var url = new URL(window.location.href);
      var name = url.searchParams.get("name");

      //request the metric
      this.metrics.forEach(element => {
        this.request_metrics(name,30,element);
      });
      
    }
    else{
      this.request_knights();
    }
    
  }
});




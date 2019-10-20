var app = new Vue({
  el: '#app',
  data: {
      message: 'Hello Vue!',
      fields: ["Meeting", "Previous Appointments (1st)", "Future Appointments (EOM)"],
      metrics: ["Associate","Insured","Postponed","Cancelled", "Available"],
      fields: [{key:'Name',sortable:true}],
      items: [],
      knights: [],
      filter: "",
      sortBy: "Meeting",
      currentKnight:"",
      hideLoading: false
      
  },
  methods: {
      test: function(){
        console.log("test");
      },
      knight_selected: function(record,indx){
        this.currentKnight = record['Name'];
        knight_url = 'knight/?name=' + this.currentKnight;
        window.location.href=knight_url;
      },
 

      request_metrics: function(name,periodical,metric, cached=false){

        //create the json with the days ago, metrics, and username
        data = {"periodical": periodical, "metrics": this.metrics, "name": name};
        
        if(cached){
          data["cached"] = "true"
        }

        //send to the current url
        axios.get('/metrics',{
          params:data
        })
          .then((response) => {
            knights_data = response.data["knights"]
            for( i=0; i< knights_data.length; i++){
              this.items.push(knights_data[i]);
              this.items.sort((a,b) => (a.Meeting > b.Meeting) ? 1 : -1 );

              //hide loading icon
              if(this.items.length == this.metrics.length){
                this.hideLoading = true;
                this.disableMetricsRequest = false;
              }
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

      logout: function(event){
        window.location.href="/logout"
      },

      generate_fields: function(){
        //go through all metrics
        this.metrics.forEach(element => {
          
          tempDict = {
            key: "Future " + element,
            sortable: true
          };

          this.fields.push(tempDict);

          tempDict = {
            key: "Past " + element,
            sortable: true
          };

          this.fields.push(tempDict);

        });

      }

  },
  mounted: function() {
      //this.request_knights();

      this.generate_fields();

      //request the metric
      this.request_metrics("all",'M',"whatever",true);

  }
});




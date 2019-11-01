var app = new Vue({
  el: '#app',
  data: {
      metrics: ["Associate","Insured","Postponed","Cancelled", "Available"],
      fields: [{key:'Name',sortable:true}],
      totalHeaders: [],
      totals:[{}],
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
 

      request_metrics: function(name,periodical,timezone, cached=false){

        //create the json with the days ago, metrics, and username
        data = {"periodical": periodical, "metrics": this.metrics, "name": name, "timezone": timezone};
        
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
              
              //add to scoreboard
              this.items.push(knights_data[i]);
              this.items.sort((a,b) => (a.Meeting > b.Meeting) ? 1 : -1 );

              //add to totals
              for(var key in knights_data[i]){
                if(this.totals[0][key]==undefined){
                  this.totals[0][key] = knights_data[i][key];
                }
                else{
                  this.totals[0][key] += knights_data[i][key];
                }
              }

              //hide loading icon
              if(this.items.length == this.metrics.length){
                this.hideLoading = true;
                this.disableMetricsRequest = false;
              }
            }
          })
          .catch(function(response){
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
          
          futureKey = "Future " + element;
          futureDict = {
            key: futureKey,
            sortable: true
          };
          this.totalHeaders.push(futureKey)
          this.fields.push(futureDict);

          pastKey = "Past " + element;
          pastDict = {
            key: pastKey,
            sortable: true
          };
          this.totalHeaders.push(pastKey)
          this.fields.push(pastDict);

        });

      }

  },
  mounted: function() {
      //this.request_knights();

      this.generate_fields();

      curr_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

      //request the metric
      this.request_metrics("all",'M',curr_timezone,true);

      
      

  }
});




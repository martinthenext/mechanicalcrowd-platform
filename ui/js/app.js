angular.module('CrudApp', [
    'xeditable'
  ])
.run(['editableOptions', '$http', function(editableOptions, $http) {

  //editable Theme
  editableOptions.theme = 'bs3';

  //   //CSRF
  // $http.defaults.headers.common['X-CSRF-Token'] = getCsrf();

  


}])

// ENABLE HTML5Mode FOR Params
.config(['$locationProvider', function($locationProvider){
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
}])

//Filter so we can inject HTML from JSON
.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
    }])

.controller('MainCtrl', MainCtrl);

MainCtrl.$inject = ['$scope', '$http', '$location'];

function MainCtrl($scope, $http, $location){

    
    
    $scope.dataSet = {
      table: {
        rows: []
      },
    };
    

    //This is for Sample Data
    $scope.sampleData = {
      upperText: "This is a sample data test",
      dataSet: {
                          upperTask: "Please consider this data entry and fix it if it’s wrong.",
                          lowerTask: "<b>Data entry is wrong if<b>:\nAddress is wrong",
                          table:
                            {
                               headers : ["Company", "Address"],
                               rows: [
                                  ["Johm Smith Ltd", "Backer str. 14"]
                               ]
                              
                            },
                          functions : ["edit", "delete"]
                }
    };


    $scope.updateRow = updateRow;

    $scope.deleteItem = deleteItem;
    
    $scope.sendAll = sendAll;

    $scope.canNotSave = canNotSave;

    $scope.isFromMturk = false;




    $scope.hasAssignment = true;
    $scope.canEdit = false;
    $scope.canDelete = false;
    $scope.errorContainer = "";

    var urlParams;

    activate();



    function activate(){

      if(!isOpenFromMTurk()){
        $scope.errorContainer = "Sorry, this page is supposed to be opened only from MTurk";
      }

      
      

      //check if we have a worker
      urlParams = $location.search();

      if(urlParams.assignmentId && urlParams.assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE'){
        $scope.hasAssignment = false;
      }
      if($scope.hasAssignment){
          $http.get('https://platform.comnsense.io/mturk/hit/', {
            params: {
              worker_id: urlParams.workerId,
              hit_id: urlParams.hitId,
              assignment_id: urlParams.assignmentId,
            },
            
          }).then(function(response){
                //parse response
                $scope.dataSet = response.data;
                $scope.csrf = response.data.token;

               

                if(_.contains($scope.dataSet.functions, 'edit')){
                  $scope.canEdit = true;      
                }
                if(_.contains($scope.dataSet.functions, 'delete')){
                  $scope.canDelete = true;      
                }


            }, function(error){
                if((error.status === 401) || (error.status === 403));
                $scope.errorContainer = "You can't accept this hit";
            });
      }


    };

    // let's check if the page is opened from Mturk
     function isOpenFromMTurk() {

        var mturk = "mturk.com";

        if (parent === window) {
          return true;
        } else {

          var referrer = document.referrer;
          var re = new RegExp(/^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i); 
          var domain = referrer.match(re) && referrer.match(re)[1];

            //check if ends with mturk.com
          if (domain.indexOf(mturk, domain.length - mturk.length) !== -1) {

            return true;
          } else {
            return false;
          }
        }



      }


    

    // Update dataSet with proper row and cell
    function updateRow(cellIndex, rowIndex, data){

        $scope.dataSet.table.rows[rowIndex][cellIndex] = data;
    }
              
   
    // Send everything as POST
    function sendAll(){

        if(!$scope.canEdit){

            alert('You can not edit, sorry');

        }
        else{
              var dataToSend = {
                  rows: $scope.dataSet.table.rows,
                  worker_id: urlParams.workerId,
                  assignment_id: urlParams.assignmentId,
                  hit_id: urlParams.hitId,
                  token: $scope.csrf,
              };
              $http.post('https://platform.comnsense.io/mturk/hit/', dataToSend
               )
                  .then(function(response){
                      alert('all good');
                  }, function(error){
                      $scope.errorContainer = "Error on sending data";
              });
        }
       
    }


    function canNotSave(){
      alert('You can not do that with sample data');
    }
    
    // Delete row
    function deleteItem(row){
        if(!$scope.canDelete){
            alert('You cannot delete!');
        }
        else{
            var index = _.indexOf($scope.dataSet.table.rows, row);
            if(index >= 0){
              $scope.dataSet.table.rows[index] = null;
            }
            else{
              alert('Row not found!');
            }
        }
        
    };
}
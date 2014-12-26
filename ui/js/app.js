var app = angular.module('uiApp', [
    'xeditable'
  ]);

app.run(['editableOptions', '$http', function(editableOptions, $http) {

  //editable Theme
  editableOptions.theme = 'bs3';

  //   //CSRF
  // $http.defaults.headers.common['X-CSRF-Token'] = getCsrf();

  


}]);

// ENABLE HTML5Mode FOR Params
app.config(['$locationProvider', function($locationProvider){
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
}]);

//Filter so we can inject HTML from JSON
app.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
    }]);

app.controller('MainCtrl', MainCtrl);

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
    $scope.smallErrorContainer = "";
    $scope.allDone = false;

    var urlParams;

    activate();


    //main function to start things up
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

          //regex to get the domain
          var referrer = document.referrer;
          var re = new RegExp(/^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i); 
          var domain = referrer.match(re) && referrer.match(re)[1];

            //check if referrer ends with mturk.com
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
              
   
    // Send data to server as POST
    function sendAll(){

        if(!$scope.canEdit){

            $scope.smallErrorContainer = 'You can not edit, sorry';

        }
        else{
              var dataToSend = {
                  token: $scope.csrf,
                  
                  mturk: {
                    worker_id: urlParams.workerId,
                    assignment_id: urlParams.assignmentId,
                    hit_id: urlParams.hitId,
                  },
                  rows: $scope.dataSet.table.rows,
                  
              };
              $http.post('https://platform.comnsense.io/mturk/hit/', dataToSend)
                  .then(function(response){
                      externalSubmit();

                  }, function(error){
                      $scope.errorContainer = "Error on sending data to server!";
              });
        }
       
    }


    //we submit this data after everything is done
    function externalSubmit(){
      $http.post('http://www.mturk.com/mturk/externalSubmit', {
        assignmentId : urlParams.assignmentId,
        success: true,
      }).then(function(response){
                      $scope.allDone = true;
                  }, function(error){
                      $scope.errorContainer = "Error on sending data to Mturk!";
              });
    }

    //Show can not save error
    function canNotSave(){
      $scope.smallErrorContainer = 'You can not do that with sample data';
    }
    
    //Delete row in table
    function deleteItem(row){
        if(!$scope.canDelete){
            $scope.smallErrorContainer = 'You cannot delete!';
        }
        else{
            var index = _.indexOf($scope.dataSet.table.rows, row);
            if(index >= 0){
              $scope.dataSet.table.rows[index] = null;
            }
            else{
              $scope.smallErrorContainer = 'Row not found!';
            }
        }
        
    };
}
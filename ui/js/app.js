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

    var urlParams;

    activate();



    function activate(){

      if(isOpenFromMTurk()){
        $scope.isFromMturk = true;
      }

          //CSRF TOKEN
      $http.get('csrf.json').then(function(response){

        $scope.csrf = response.data.token;

      }, function(error){
        $scope.csrf = null;
      });
      

      //check if we have a worker
      urlParams = $location.search();

      if(urlParams.assignmentId && urlParams.assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE'){
        $scope.hasAssignment = false;
      }
      if($scope.hasAssignment){
          $http.get('data.json').then(function(response){
                //parse response
                $scope.dataSet = response.data;

               

                if(_.contains($scope.dataSet.functions, 'edit')){
                  $scope.canEdit = true;      
                }
                if(_.contains($scope.dataSet.functions, 'delete')){
                  $scope.canDelete = true;      
                }


            }, function(error){
                alert("Houston, we've got a problem! Check the console to see what's up" );
                console.log(error);
            });
      }


    };

    // let's check if the page is opened from Mturk
     function isOpenFromMTurk() {
        var re = /mturk.com/;
        if (window.self === window.top) {
          return false;
        } else {
          if (re.test(document.referrer)) {
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
                  worker_id: urlParams.worker_id,
                  assignment_id: urlParams.assignment_id,
                  hit_id: urlParams.hit_id,
              };
              $http.post('response.json', dataToSend, 
                {
                  headers: {'X-CSRF-Token': $scope.csrf},
                })
                  .then(function(response){
                      alert('all good');
                  }, function(error){
                      alert("Houston, we've got a problem! Check the console to see what's up" );
                      console.log(error);
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
            $scope.dataSet.table.rows = _.without($scope.dataSet.table.rows, row);
        }
        
    };
}
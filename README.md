# REST v1

## resource /api/v1/auth/token
### POST
Login user and returns token

    ~: user$ curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":"admin"}' http://localhost:8000/api/v1/auth/token/; echo
        
    {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0MTg3NjM2NTMsInVzZXJfaWQiOjEsImVtYWlsIjoia2lyaWxsQGdvbGRzaHRlaW4ub3JnIiwidXNlcm5hbWUiOiJyb3NzbyJ9.4qMfre4d6OfKVK4Fo8wtc7s1XMlb1rBie5FONvY71HM"}
    ~: user$ 
    
Useful in console

    ~: user$ TOKEN=`curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}' http://localhost:8000/api/v1/auth/token/ | sed -e 's/{"token": "//g' -e 's/"}//g'`

## resource /api/v1/xlsx/
### GET

Return list of uploaded XLSX files, without binary data

    ~: user$ curl -X GET \
        -H 'Allow: application/json' \
        -H "Authorization: Key $TOKEN" http://localhost:8000/api/v1/xlsx/; echo
        
    [{"id": 1, "owner": "admin", "filename": "test.xlsx", "sheets": ["first", "second", "third"]}]
    ~: user$
    
### POST

Upload new table to service

    +icebook ~: rosso$ curl -X POST \
        -H 'Content-Disposition:attachment; filename=test.xlsx' \
        -H 'Allow: application/json' \
        -H 'Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
        -H "Authorization: Key $TOKEN" \
        --data-binary @/path/to/table.xlsx http://localhost:8000/api/v1/xlsx/ ; echo
        
    {"id": 1, "owner": "admin", "filename": "test.xlsx", "sheets": ["first", "second", "third"]}
    
    
## resource /api/v1/xlsx/\<id\>/

### GET

Return uploaded file metadata

    ~: user$ curl -X GET \
        -H 'Allow: application/json' \
        -H "Authorization: Key $TOKEN" http://localhost:8000/api/v1/xlsx/1/; echo
        
    [{"id": 1, "owner": "admin", "filename": "test.xlsx", "sheets": ["first", "second", "third"]}]
    ~: user$
    

## resource /api/v1/task/

### GET

List existing tasks

    ~: user$ curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN" http://localhost:8000/api/v1/task/; echo
    
    [{"sheet": "first", "columns": "Company,Address,Zip,City,Province", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "id": 1, "table": 2}, {"sheet": "first", "columns": "Company,Address", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "id": 2, "table": 2}]
    ~: user$ 

### POST

Create new task

    ~: user$ curl -X POST \
        -H 'Allow: application/json' \
        -H "Authorization: Key $TOKEN" \
        -H 'Content-type: application/json' \
        -d '{"sheet": "first", "columns": "Company,Address", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "table": 2}' http://localhost:8000/api/v1/task/; echo
        
    {"sheet": "first", "columns": "Company,Address", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "id": 2, "table": 2}
    ~: user$ 
    
## resource /api/v1/task/\<id\>

### GET

Return task description

    ~: user$ curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN" http://localhost:8000/api/v1/task/2; echo
    
    {"sheet": "first", "columns": "Company,Address", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "id": 2, "table": 2}
    ~: user$
    
### PUT

Change task

    ~: user$ curl -X PUT \
        -H 'Allow: application/json' \
        -H "Authorization: Key $TOKEN" \
        -H 'Content-type: application/json' \
        -d '{"sheet": "first", "columns": "Company,Address,Zip", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "table": 2}' http://localhost:8000/api/v1/task/2/; echo
        
    {"sheet": "all potential customers", "columns": "Company,Address,Zip", "header_location": "C1:AU1", "data_location": "C3:", "wrong_rows_definition": "", "task_definition": "", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "id": 2, "table": 2}
    ~: user$
    
### DELETE

Delete task

    ~: user$ curl -X DELETE -H 'Allow: application/json' -H "Authorization: Key $TOKEN" http://localhost:8000/api/v1/task/2; echo
    ~: user$
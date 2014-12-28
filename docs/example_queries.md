# Comnsense platform example queries

This document contains a series of example quereies made to Comnsense platform where the platform user `stasik` uploads the Excel table, marks the tasks, puts them on Mechanical Turk and gathers results of worker's input. This is now a full description of API methods: ones used to view available tables/tasks/etc are ommited and only the cruicial ones are described.

Sensitive information is masked. Queries are made with `curl` for demonstration and testing purposes. In production it's easier to send HTTP requests from Python directly.

First, user enters the VPN network of the platform.

User authentificates using password to get an access token it can use for later queries.

    user$ TOKEN=`curl -X POST -H "Content-Type: application/json" \
      -d '{"username":"mcrowd","password":"XXXXXX"}' \
      http://platform.inner.comnsense.io/api/v1/auth/token/ \
      | sed -e 's/{"token": "//g' -e 's/"}//g'`
    user$ echo $TOKEN
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im5vLXJlcGx5QGNvbW5zZW5zZS5pbyIsInVzZXJfaWQiOjIsImV4cCI6MTQyMDQwMDE2OSwidXNlcm5hbWUiOiJtY3Jvd2QifQ.DZT3_LapS3DeUN9JDrJylaMo1gD3848L9qcc3em3cek

User uploads an `.xlsx` file.

    user$ curl -X POST -H 'Content-Disposition:attachment; filename=test.xlsx' \
      -H 'Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
      -H "Authorization: Key $TOKEN" \
      --data-binary @$PWD/Downloads/safari/Address_DataBase_from_Italy_for_Migration_DO-09-0009726_a_1.xlsx \
      http://platform.inner.comnsense.io/api/v1/xlsx/
    {"id": 1, "owner": "mcrowd", "filename": "address.xlsx", "sheets": [{"name": "address.xlsx!all potential customers", "number": 0}, {"name": "address.xlsx!not migrated addresses", "number": 1}, {"name": "address.xlsx!Contact_Persons", "number": 2}, {"name": "address.xlsx!Translation values", "number": 3}]}

Now the uploaded file is available at `/api/v1/xlsx/1`. User views the available worksheet names:

    user$ curl -X GET -H 'Allow: application/json' \
      -H "Authorization: Key $TOKEN" \
      http://platform.inner.comnsense.io/api/v1/xlsx/1/worksheets/ \
    [{"name": "address.xlsx!all potential customers", "number": 0}, {"name": "address.xlsx!not migrated addresses", "number": 1}, {"name": "address.xlsx!Contact_Persons", "number": 2}, {"name": "address.xlsx!Translation values", "number": 3}]

User sees that table of interest is located on a worksheet `all potential customers`, header is located from cell `A1` to cell `K1` and data starts at `A3`. He then registers a `table` with this information:

    user$ curl -X POST -H 'Allow: application/json' \ 
      -H "Authorization: Key $TOKEN"  \
      -H 'Content-type: application/json' \ 
      -d '{"worksheet": "test.xlsx!all potential customers", "header_location": "A1:AU1", "data_location": "A3:"}' \
      http://platform.inner.comnsense.io/api/v1/xlsx/1/worksheets/0/tables/
    {"worksheet": "address.xlsx!all potential customers", "col_names": ["", "", "Nr. client", "Source", "Company type", "", "Company", "Address", "Zip", "City", "Province", "Telephone", "Fax", "email", "web site", "contact name 1", "contact surname 1", "contact function 1", "Cell phone 1", "email 1", "", "", "", "", "", "", "", "", "", "", "core business", "turnover 2002", "employees", "VAT Nr.", "tax payer account Nr.", "certification", "certification data", "founding year", "note", "construction site done", "next construcion site", "trade info", "action 1", "", "", "", ""], "col_ids": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU"], "header_location": "A1:AU1", "data_location": "A3:", "id": 1}

The table now lives at `/api/v1/xlsx/1/worksheets/0/tables/1`. User now creates a task for this table:

    user$ curl -X POST -H 'Allow: application/json' \
      -H "Authorization: Key $TOKEN" \
      -H 'Content-type: application/json' \
      -d '{
        "table": 1, 
        "columns": "Address,Company,Zip", 
        "task_definition": "check adrress and fix it"}' \
      http://platform.inner.comnsense.io/api/v1/task/
    {"table": 1, "columns": "Company,Address,Zip", "wrong_rows_definition": "", "task_definition": "check adrress and fix it", "deduplicate": false, "edit_allowed": true, "delete_allowed": true, "active": false, "hits_per_user": 1, "id": 3}

Task lives at `/api/v1/task/1/`, table attached to it is identified by `/api/v1/task/1/table/`. **Now all actions with this tasks are performed in terms of `diff`s - changes to the original table in the context of the task.** For example, the user can submit a change to the table:

    user$ curl -X POST -H 'Content-type: application/json' 
      -H "Authorization: Key $TOKEN"  
      -d '{"row_diff": [[12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]]],
        "meta_diff": [{"submit": true}]}' http://platform.inner.comnsense.io/api/v1/task/1/diff/

These diffs can be then retrieved:

    user$ curl -X GET \
      -H "Authorization: Key $TOKEN"  \
      http://platform.inner.comnsense.io/api/v1/task/1/diff/
    {"row_diff": [[12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]]],"meta_diff": [{"submit": true}]}

If there are conflicts, as in one table row is affected multiple times, user can retrieve only the last change:

    user$ curl -X GET -H 'Allow: application/json' \
      -H "Authorization: Key $TOKEN"  \
      http://platform.inner.comnsense.io/api/v1/task/1/diff/?aggregated
    {"row_diff": [[12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]]], "meta_diff": [{"submit": true}]}

Submit all selected rows to mturk

    user$ curl -X POST \
      -H "Authorization: Key $TOKEN" \
      http://platform.inner.comnsense.io/api/v1/task/1/submit/; echo
    [{"ident": "3UZUVSO3P73NK1CVH054A4LP8UBMES", 
        "url": "https://workersandbox.mturk.com/mturk/preview?groupId=3Z5V3T2EPUC1VVNJO8VZOX7DUYO7L2"}]

Results of MTurk workers' input are retrieved:

    curl -X GET \
      -H "Authorization: Key $TOKEN"  \
      http://platform.inner.comnsense.io/api/v1/task/1/diff/
    
    {
      "meta_diff": [
        {"submit": true, "user": "stasik"},
        {"assignment": 1, "turker": 1, "hit": 1},
        {"assignment": 2, "turker": 2, "hit": 1},
        {"assignment": 3, "turker": 3, "hit": 1}
      ], 
      "row_diff": [
        [12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]],
        [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 5", 23823]],
        [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 6", 23823]],
        [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 7", 23823]]
      ]
    }

First diff means that user `stasik` has marked the row `12981` for submition, other 3 are responses from MTurk workers.

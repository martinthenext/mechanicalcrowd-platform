# Comnsense platform example queries

This document contains a series of example quereies made to Comnsense platform where the platform user `stasik` uploads the Excel table, marks the tasks, puts them on Mechanical Turk and gathers results of worker's input. This is now a full description of API methods: ones used to view available tables/tasks/etc are ommited and only the cruicial ones are described.

Sensitive information is masked. Queries are made with `curl` for demonstration and testing purposes. In production it's easier to send HTTP requests from Python directly.

First, user enters the VPN network of the platform.

User authentificates using password to get an access token it can use for later queries.

    TOKEN=`curl -X POST -H "Content-Type: application/json" -d '{"username":"stasik","password":"XXXXXX"}' -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/auth/token/ | sed -e 's/{"token": "//g' -e 's/"}//g'`
    echo $TOKEN

User uploads an `.xlsx` file.

    curl -X POST -H 'Content-Disposition:attachment; filename=test.xlsx' -H 'Allow: application/json' -H 'Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' -H "Authorization: Key $TOKEN" --data-binary @$PWD/Downloads/safari/Address_DataBase_from_Italy_for_Migration_DO-09-0009726_a_1.xlsx -H 'Host: plarform.inner.comnsense.io' http://10.8.2.1/api/v1/xlsx/

Now the uploaded file is available at `/api/v1/xlsx/1`. User views the available worksheet names:

    curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/xlsx/1/worksheets/

User sees that table of interest is located on a worksheet `all potential customers`, header is located from cell `A1` to cell `K1` and data starts at `A3`. He then registers a `table` with this information:

    curl -X POST -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Content-type: application/json' -d '{"worksheet": "test.xlsx!all potential customers", "header_location": "A1:K1", "data_location": "A3:"}' -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/xlsx/1/worksheets/0/tables/

The table now lives at `/api/v1/xlsx/1/worksheets/0/tables/1`. User now creates a task for this table:

    curl -X POST -H 'Allow: application/json' -H 'Content-type: application/json' -d '{"table": 1, "columns": "Address,Company,Zip", "task_definition": "check adrress and fix it"}' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/task/

Task lives at `/api/v1/task/1/`, table attached to it is identified by `/api/v1/task/1/table/`. **Now all actions with this tasks are performed in terms of `diff`s - changes to the original table in the context of the task.** For example, the user can submit a change to the table:

    curl -X POST -H 'Content-type: application/json' -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' -d '{"row_diff": [[12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]]], "meta_diff": [{"submit": true}]}' http://10.8.2.1/api/v1/task/1/diff/

These diffs can be then retrieved:

    curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/task/1/diff/

If there are conflicts, as in one table row is affected multiple times, user can retrieve only the last change:

    curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/task/1/diff/?aggregated

*TODO: Here adding `submit=True` on row `12981` and submitting it on MTurk should be described*

Results of MTurk workers' input are retrieved:

    curl -X GET -H 'Allow: application/json' -H "Authorization: Key $TOKEN"  -H 'Host: platform.inner.comnsense.io' http://10.8.2.1/api/v1/task/1/diff/
    
    {"meta_diff": [{"submit": true, "user": "stasik"}, {"assignment": 1, "turker": 1, "hit": 1}, {"assignment": 2, "turker": 2, "hit": 1}, {"assignment": 3, "turker": 3, "hit": 1}], "row_diff": [[12981, ["Immobiliare \"San Giorgio\" srl", "Via Mazzini,3", 23823]], [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 5", 23823]], [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 6", 23823]], [12981, ["Immobiliare \"San Giorgio\" srl", "Via Di Mazzini, 7", 23823]]]}


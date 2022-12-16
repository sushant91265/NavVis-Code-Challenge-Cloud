#!/bin/bash

# run docker compose in the background
docker-compose -f server/docker-compose.yml up --build -d

# wait for the database to be ready
sleep 100

printf "\n***********Running integration tests***********\n"
PASS=0
FAIL=0

printf "\nhit the '/ping' endpoint and check the response to be pong\n"
ping_output=$(curl -s http://localhost:8000/ping | jq -r '.message')
if [ "$ping_output" != "pong" ]; then
    echo "Expected pong, got $ping_output, Test failed!"
    FAIL=$((FAIL+1))
else
    echo "Test passed!"
    PASS=$((PASS+1))
fi

printf "\nhit the '/upload' endpoint and get the task id from the response\n"
upload_output=$(curl -X 'POST' \
  'http://localhost:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@phone_numbers_8.txt;type=text/plain')
task_id=$(echo $upload_output | jq -r '.task')

if [[ -n "$task_id" ]]; then
    echo "Test passed!"
    PASS=$((PASS+1))
else
    echo "Expected task id, got $task_id, Test failed!"
    FAIL=$((FAIL+1))
fi

printf "\nhit the '/tasks' endpoint to get the list of tasks\n"
tasks_output=$(curl -X 'GET' \
  'http://localhost:8000/tasks' \
  -H 'accept: application/json' | jq -r '.items')

if [[ -z "$tasks_output" ]]; then
    echo "Expected list of tasks, got $tasks_output, Test failed!"
    FAIL=$((FAIL+1))
else
    echo "Test passed!"
    PASS=$((PASS+1))
fi

printf "\nhit the '/tasks/{task_id}' endpoint to get the task details\n"
task_output=$(curl -X 'GET' \
  "http://localhost:8000/tasks/$task_id/results" \
  -H 'accept: application/json' | jq -r '.items.phone_number')

if [[ -n "$task_output" ]]; then
    echo "Test passed!"
    PASS=$((PASS+1))
else
    echo "Expected list of phone numbers, got $task_output, Test failed!"
    FAIL=$((FAIL+1))
fi

printf "\nhit the delete endpoint to delete the task results\n"
delete_output=$(curl -X 'DELETE' \
  "http://localhost:8000/tasks/$task_id/results" \
  -H 'accept: application/json' | jq -r '.status')

if [[ "$delete_output" == "success" ]]; then
    # hit the /tasks/{task_id} endpoint to get the task details
    delete_task_output=$(curl -X 'GET' \
      "http://localhost:8000/tasks/$task_id/results" \
      -H 'accept: application/json' | jq -r '.items')
    if [[ "$delete_task_output" != "null" ]]; then
        echo "Expected empty list of phone numbers, got $delete_task_output, Test failed!"
        FAIL=$((FAIL+1))
    else
        echo "Test passed!"
        PASS=$((PASS+1))
    fi   
else
    echo "Expected success, got $delete_output, Test failed!"
    FAIL=$((FAIL+1))
fi

printf "\nTests passed: %s Tests failed: %s" $PASS $FAIL 
printf "\n"
printf "\n***********Stopping docker compose***********\n"


docker-compose -f server/docker-compose.yml down

sleep 10

exit 1

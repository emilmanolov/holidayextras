#!/bin/sh
curl -i -H "Accept: application/json" -X GET http://localhost:8000/user/1
curl -i -H "Accept: application/json"-H "Content-Type: application/json" -X POST -d '{"email":"user1@gmail.com","forename":"user1","surname":"user1"}' http://localhost:8000/user/
curl -i -H "Accept: application/json"-H "Content-Type: application/json" -X PUT -d '{"email":"user111@mail.com","forename":"user111","surname":"user111"}' http://localhost:8000/user/1
curl -i -X DELETE http://localhost:8000/user/1

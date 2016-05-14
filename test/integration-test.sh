#!/bin/sh
curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/user/1
curl -i -H "Content-Type: application/json" -X POST -d '{"email":"emo@mail.com","forename":"emo1","surname":"emo2"}' http://localhost:8000/user/
curl -i -H "Content-Type: application/json" -X PUT -d '{"email":"emo22222@mail.com","forename":"emo1111","surname":"emo2"}' http://localhost:8000/user/1
curl -i -H "Content-Type: application/json" -X DELETE http://localhost:8000/user/1

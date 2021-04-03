## Dockerized Async Todo List with FastAPI, persisting data in Mongo (cloud) and PgSQL (Docker-compose)
## Soon: + MongoDB (Docker-compose) + Redis (Docker-compose)

## Remember edit .env file with your DB string connections and all that stuff.
## For connect Mongo Cloud Free Service you have to get an account on cloud.mongodb.com and
## get the string connection and put into the .env file

## For run the application you have to run in your terminal inside the main folder:
## docker-compose up --build

## For PostgreSQL migrations run:
## Once the docker-compose is up, you have yo run inside the container "fastapi-todolist":
## docker exec -ti fastapi-todolist alembic upgrade head
## this do the migrations to the PostreSQL server and set all ready for use

## For Run 

###### Author: Leonardo Hakim <leohakim@gmail.com>

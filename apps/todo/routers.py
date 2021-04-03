from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config import settings
from datetime import datetime
import uuid

from .models import TaskModel, UpdateTaskModel

router = APIRouter()


# todo: Fix coupled TABLE NAME
@router.post("/", response_description="Add new task")
async def create_task(request: Request, task: TaskModel = Body(...)):
    task = jsonable_encoder(task)

    # MongoDB Async Insertion
    new_task = await request.app.mongodb["tasks"].insert_one(task)
    created_task = await request.app.mongodb["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )

    # PostgreSQL Async Insert
    task["id"] = str(task.pop("_id", False))
    task["timestamp"] = datetime.strptime(task["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
    query = f"""INSERT INTO todolist2 (id, name, timestamp, completed)
        VALUES (:id, :name, :timestamp, :completed)
        """
    new_task_pgsql = await request.app.state.pgsql_db.execute(query=query, values=task)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


# todo: Fix coupled TABLE NAME
@router.get("/", response_description="List all tasks")
async def list_tasks(request: Request):
    # MongoDB List
    tasks = []
    for doc in await request.app.mongodb["tasks"].find().to_list(length=100):
        tasks.append(doc)
    # return tasks

    # PostgreSQL List
    tasks_pgsql = []
    query = "SELECT * FROM todolist2 ORDER BY timestamp DESC"
    for task in await request.app.state.pgsql_db.fetch_all(query=query):
        tasks_pgsql.append(task)
    return tasks


# todo: Fix coupled TABLE NAME
@router.get("/{id}", response_description="Get a single task")
async def show_task(id: str, request: Request):
    # uuid validation
    try:
        val = uuid.UUID(id, version=4)
    except ValueError:
        return "Not valid id (uuid field)"

    #  MongoDB Retrieve
    if (task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
        return task

    # PostgreSQL Retrieve

    query = "SELECT * FROM todolist2 WHERE id = :id"
    if (task_pgsql := await request.app.state.pgsql_db.fetch_one(query=query, values={"id": id})) is not None:
        return task_pgsql

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


# todo: Fix coupled TABLE NAME
@router.put("/{id}", response_description="Update a task")
async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    # uuid validation
    try:
        val = uuid.UUID(id, version=4)
    except ValueError:
        return "Not valid id (uuid field)"
    # MongoDB Update
    task = {k: v for k, v in task.dict().items() if v is not None}
    if len(task) >= 1:
        update_result = await request.app.mongodb["tasks"].update_one(
            {"_id": id}, {"$set": task}
        )

        if update_result.modified_count == 1:
            if (
                    updated_task := await request.app.mongodb["tasks"].find_one({"_id": id})
            ) is not None:
                pass

    if (
            existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})
    ) is not None:
        pass

    # PostgreSQL Update
    # todo: Refactor Update Query and coupling table name
    name = task['name'] if 'name' in task else None
    completed = task['completed'] if 'completed' in task else None
    if name is None and completed is None:
        return "You must change something!"
    if name is not None and completed is not None:
        query = f"UPDATE todolist2 SET name='{name}', completed='{completed}' WHERE id = '{id}'"
    elif name is not None:
        query = f"UPDATE todolist2 SET name='{name}' WHERE id = '{id}'"
    elif completed is not None:
        query = f"UPDATE todolist2 SET completed={completed} WHERE id = '{id}'"
    update_task_pgsql = await request.app.state.pgsql_db.execute(query=query)

    query = "SELECT * FROM todolist2 WHERE id = :id"
    if (task_pgsql := await request.app.state.pgsql_db.fetch_one(query=query, values={"id": id})) is not None:
        pass

    if updated_task:
        return updated_task
    if existing_task:
        return existing_task
    if task_pgsql:
        return task_pgsql

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


# todo: decoupling table name
@router.delete("/{id}", response_description="Delete Task")
async def delete_task(id: str, request: Request):
    try:
        val = uuid.UUID(id, version=4)
    except ValueError:
        return "Not valid id (uuid field)"

    delete_mongo, delete_pgsql = False, False
    delete_result = await request.app.mongodb["tasks"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        delete_mongo = True

    query = f"DELETE FROM todolist2 WHERE id = '{id}'"
    delete_result = await request.app.state.pgsql_db.execute(query=query)
    if delete_result is None:
        delete_pgsql = True

    if not delete_pgsql:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"PostgreSQL couldn\'t delete the task.")

    if not delete_mongo:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"MongoDB couldn\'t delete the task.")

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

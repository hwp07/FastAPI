from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
import re
from datetime import datetime

app = FastAPI(
    title="Team Task Manager API",
    description="Hệ thống quản lý công việc nhóm sử dụng FastAPI",
    version="1.0.0"
)

tasks_db = []

class ApiResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    path: str

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=2)
    priority: int = Field(..., ge=1, le=5)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class TaskPublicResponse(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = None
    assignee: Optional[str] = Field(None, min_length=2)
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v and v not in ["todo", "in_progress", "done"]:
            raise ValueError("Invalid status")
        return v

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    error_code = "ERR-VAL-422" if exc.status_code == 422 else f"ERR-{exc.status_code}"
    response = ApiResponse(
        statusCode=exc.status_code,
        message=str(exc.detail) if isinstance(exc.detail, str) else "Lỗi hệ thống",
        data=None,
        error=f"{error_code}: {exc.detail}",
        timestamp=datetime.now().isoformat() + "Z",
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    response = ApiResponse(
        statusCode=422,
        message="Lỗi: Dữ liệu đầu vào sai định dạng hoặc thiếu trường bắt buộc!",
        data=None,
        error="ERR-VAL-422: Validation error: Input json parameters datatype hints mismatch or core required fields missing.",
        timestamp=datetime.now().isoformat() + "Z",
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=422,
        content=response.model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    response = ApiResponse(
        statusCode=500,
        message="Lỗi hệ thống nội bộ không mong muốn",
        data=None,
        error=f"ERR-INTERNAL: {str(exc)}",
        timestamp=datetime.now().isoformat() + "Z",
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=500,
        content=response.model_dump()
    )

def find_task_index(task_id: int) -> Optional[int]:
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            return idx
    return None

def generate_task_id() -> int:
    if not tasks_db:
        return 1
    return max(task["id"] for task in tasks_db) + 1

def check_title_duplicate(title: str, exclude_id: Optional[int] = None) -> bool:
    for task in tasks_db:
        if task["title"].lower() == title.lower() and task["id"] != exclude_id:
            return True
    return False

@app.post("/tasks", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreateSchema):
    if check_title_duplicate(task.title):
        raise HTTPException(
            status_code=400,
            detail="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!"
        )

    new_task = {
        "id": generate_task_id(),
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "priority": task.priority,
        "status": "todo",
        "created_at": datetime.now().isoformat() + "Z",
        "internal_notes": ""
    }

    tasks_db.append(new_task)

    public_task = TaskPublicResponse(**new_task)

    return ApiResponse(
        statusCode=201,
        message="Tạo mới công việc nhóm thành công!",
        data=public_task.model_dump(),
        error=None,
        timestamp=datetime.now().isoformat() + "Z",
        path="/tasks"
    )

@app.get("/tasks/search", response_model=ApiResponse)
async def search_tasks(
    keyword: Optional[str] = Query(None, description="Từ khóa tìm kiếm"),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái")
):
    filtered_tasks = []

    for task in tasks_db:
        match_keyword = True
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            match_keyword = (
                pattern.search(task["title"]) is not None or
                pattern.search(task["assignee"]) is not None
            )

        match_status = True
        if status:
            match_status = task["status"] == status

        if match_keyword and match_status:
            public_task = TaskPublicResponse(**task)
            filtered_tasks.append(public_task.model_dump())

    return ApiResponse(
        statusCode=200,
        message="Tìm kiếm công việc thành công",
        data={
            "total": len(filtered_tasks),
            "tasks": filtered_tasks
        },
        error=None,
        timestamp=datetime.now().isoformat() + "Z",
        path="/tasks/search"
    )

@app.get("/tasks/{task_id}", response_model=ApiResponse)
async def get_task(task_id: int = Path(..., gt=0)):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!"
        )

    task = tasks_db[index]
    public_task = TaskPublicResponse(**task)

    return ApiResponse(
        statusCode=200,
        message="Lấy thông tin công việc thành công",
        data=public_task.model_dump(),
        error=None,
        timestamp=datetime.now().isoformat() + "Z",
        path=f"/tasks/{task_id}"
    )

@app.put("/tasks/{task_id}", response_model=ApiResponse)
async def update_task(update_data: TaskUpdateSchema, task_id: int = Path(..., gt=0)):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!"
        )

    task = tasks_db[index]

    if update_data.title and check_title_duplicate(update_data.title, task_id):
        raise HTTPException(
            status_code=400,
            detail="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!"
        )

    if update_data.status and update_data.status not in ["todo", "in_progress", "done"]:
        raise HTTPException(
            status_code=400,
            detail="Lỗi: Trạng thái công việc cập nhật không đúng quy định!"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if key != "status" or value:
            task[key] = value

    if "status" in update_dict:
        task["status"] = update_dict["status"]

    public_task = TaskPublicResponse(**task)

    return ApiResponse(
        statusCode=200,
        message="Cập nhật công việc thành công",
        data=public_task.model_dump(),
        error=None,
        timestamp=datetime.now().isoformat() + "Z",
        path=f"/tasks/{task_id}"
    )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int = Path(..., gt=0)):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!"
        )

    tasks_db.pop(index)
    return None


@app.get("/")
async def root():
    return {"message": "Team Task Manager API is running. Access /docs for Swagger UI."}


from fastapi import FastAPI

app = FastAPI()

database = [
    {
        "id": 1,
        "title": "Python Basics",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2020,
        "is_available": True,
    },
    {
        "id": 2,
        "title": "Learning SQL",
        "author": "Tran Thi B",
        "category": "database",
        "year": 2019,
        "is_available": False,
    },
    {
        "id": 3,
        "title": "HTML & CSS",
        "author": "Le Van C",
        "category": "web",
        "year": 2021,
        "is_available": True,
    },
    {
        "id": 4,
        "title": "Computer Networks",
        "author": "Pham Van D",
        "category": "network",
        "year": 2018,
        "is_available": False,
    },
    {
        "id": 5,
        "title": "Java Programming",
        "author": "Hoang Thi E",
        "category": "programming",
        "year": 2022,
        "is_available": True,
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2023,
        "is_available": True,
    },
]


@app.get("/books/statistics")
def get_statistic_books():
    cnt_available = 0
    cnt_borrow = 0
    for i in database:
        if i["is_available"] is True:
            cnt_available += 1
        else:
            cnt_borrow += 1

        return {
            "total_books": len(database),
            "available_books": cnt_available,
            "borrowed_books": cnt_borrow,
        }


# tạo 1 mảng rỗng duyệt qua danh sách check xem có thuộc mảng rỗng ko không thuộc thì nó cho vào mảng rỗng thế là chỉ lấy mỗi cái 1 lần duy nhất tại có rồi nó sẽ ko thêm nx
@app.get("/books/categories")
def get_catergory_book():
    list = []
    for i in database:
        if i["category"] not in list:
            list.append(i)

    return {"catergory": list}


@app.get("/books/latest")
def get_max_books():
    max = 0
    for i in database:
        if i["year"] > max:
            max = i["year"]
            a = i
    return {"message": "Sách có năm lớn nhất", "data": a}


# cách 2
@app.get("/books/latest")
def sort_database():
    database.sort(lambda book: book["year"], reverse=True)
    return database


# cách 3
@app.get("/books/latest")
def sort_databases():
    database.sort(lambda book: -book["year"])
    return database


# cách 4
@app.get("/books/latest")
def sort_databasess():
    database.sort(lambda book: book["year"])
    database[::-1]
    return database
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
def get_statistics():
    available_books = 0
    borrowed_books = 0

    for book in database:
        if book["is_available"]:
            available_books += 1
        else:
            borrowed_books += 1

    return {
        "total_books": len(database),
        "available_books": available_books,
        "borrowed_books": borrowed_books,
    }

@app.get("/books/categories")
def get_categories():
    categories = []

    for book in database:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {
        "total_categories": len(categories),
        "categories": categories,
    }

@app.get("/books/latest")
def get_latest_book():
    latest_book = database[0]

    for book in database:
        if book["year"] > latest_book["year"]:
            latest_book = book

    return {
        "message": "Sách mới nhất",
        "data": latest_book,
    }

@app.get("/books/sort-desc")
def sort_books_desc():
    sorted_books = sorted(database,key=lambda book: book["year"],reverse=True)
    return sorted_books

@app.get("/books/sort-asc")
def sort_books_asc():
    sorted_books = sorted(database,key=lambda book: book["year"])
    return sorted_books
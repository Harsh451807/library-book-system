# ============================================================================
#  📚 CITY PUBLIC LIBRARY — FastAPI Backend
#  All 20 Questions | Day 1–Day 6 Concepts
# ============================================================================

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import math

# ── Q1: Create FastAPI app ──────────────────────────────────────────────────
app = FastAPI(
    title="City Public Library",
    description="Library Book Management System — FastAPI Project"
)

# ============================================================================
#  📦 IN-MEMORY DATA
# ============================================================================

# ── Q2: Books list (8 books, 4 genres) ─────────────────────────────────────
books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Fiction",
        "is_available": True,
    },
    {
        "id": 2,
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "genre": "Science",
        "is_available": True,
    },
    {
        "id": 3,
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "genre": "History",
        "is_available": True,
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": "Tech",
        "is_available": True,
    },
    {
        "id": 5,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Fiction",
        "is_available": True,
    },
    {
        "id": 6,
        "title": "The Selfish Gene",
        "author": "Richard Dawkins",
        "genre": "Science",
        "is_available": True,
    },
    {
        "id": 7,
        "title": "1984",
        "author": "George Orwell",
        "genre": "Fiction",
        "is_available": True,
    },
    {
        "id": 8,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "genre": "Tech",
        "is_available": True,
    },
]

# ── Q4: Borrow records list + counter ──────────────────────────────────────
borrow_records = []
record_counter = 1

# ── Q14: Borrow queue (waitlist) ───────────────────────────────────────────
queue = []


# ============================================================================
#  📐 PYDANTIC MODELS  (Day 2 — Q6, Q9, Q11)
# ============================================================================

# ── Q6 + Q9: BorrowRequest ─────────────────────────────────────────────────
#   Q6  → member_name, book_id, borrow_days(gt=0), member_id
#   Q9  → added member_type; premium may borrow up to 60 days
class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2, description="Name of the library member")
    book_id: int = Field(..., gt=0, description="ID of the book to borrow")
    borrow_days: int = Field(
        ...,
        gt=0,
        le=60,
        description="Number of days (regular ≤30, premium ≤60)",
    )
    member_id: str = Field(..., min_length=4, description="Member card ID")
    member_type: str = Field(
        default="regular",
        description="'regular' or 'premium'",
    )


# ── Q11: NewBook ───────────────────────────────────────────────────────────
class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = Field(default=True)


# ============================================================================
#  🔧 HELPER FUNCTIONS  (Day 3 — Q7, Q9, Q10)
#  Plain functions — NO @app decorator
# ============================================================================

# ── Q7: find_book ──────────────────────────────────────────────────────────
def find_book(book_id: int):
    """Return the book dict if found, else None."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None


# ── Q7 + Q9: calculate_due_date ────────────────────────────────────────────
def calculate_due_date(borrow_days: int, member_type: str = "regular") -> str:
    """
    Premium members → allowed up to 60 days.
    Regular members → capped at 30 days.
    Returns a human-readable due-date string.
    """
    base_day = 15
    if member_type == "premium":
        effective_days = min(borrow_days, 60)
    else:
        effective_days = min(borrow_days, 30)
    return f"Return by: Day {base_day + effective_days}"


# ── Q10: filter_books_logic ────────────────────────────────────────────────
def filter_books_logic(
    genre: str = None,
    author: str = None,
    is_available: bool = None,
):
    """Filter the global books list. Uses 'is not None' for each check."""
    results = books.copy()
    if genre is not None:
        results = [b for b in results if b["genre"].lower() == genre.lower()]
    if author is not None:
        results = [b for b in results if b["author"].lower() == author.lower()]
    if is_available is not None:
        results = [b for b in results if b["is_available"] == is_available]
    return results


# ============================================================================
#  🌐 ROUTES
#  ⚠ RULE: all fixed paths BEFORE any /{id} variable paths
# ============================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q1 — GET /  (Home Route)                                        Day 1
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q2 — GET /books  (All books + counts)                           Day 1
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books")
def get_all_books():
    available_count = sum(1 for b in books if b["is_available"])
    return {
        "total": len(books),
        "available_count": available_count,
        "books": books,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q5 — GET /books/summary  (above /books/{book_id})               Day 1
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/summary")
def get_books_summary():
    total = len(books)
    available = sum(1 for b in books if b["is_available"])
    borrowed = total - available
    genre_breakdown = {}
    for book in books:
        g = book["genre"]
        genre_breakdown[g] = genre_breakdown.get(g, 0) + 1
    return {
        "total_books": total,
        "available_count": available,
        "borrowed_count": borrowed,
        "genre_breakdown": genre_breakdown,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q10 — GET /books/filter                                         Day 3
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/filter")
def filter_books(
    genre: Optional[str] = None,
    author: Optional[str] = None,
    is_available: Optional[bool] = None,
):
    results = filter_books_logic(genre, author, is_available)
    return {"count": len(results), "books": results}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q16 — GET /books/search  (keyword, case-insensitive)            Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/search")
def search_books(keyword: str = Query(..., min_length=1)):
    kw = keyword.lower()
    results = [
        b
        for b in books
        if kw in b["title"].lower() or kw in b["author"].lower()
    ]
    if not results:
        return {
            "message": f"No books found matching '{keyword}'",
            "total_found": 0,
            "results": [],
        }
    return {"keyword": keyword, "total_found": len(results), "results": results}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q17 — GET /books/sort                                           Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/sort")
def sort_books(
    sort_by: str = Query(default="title"),
    order: str = Query(default="asc"),
):
    valid_fields = ["title", "author", "genre"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        return {"error": f"Invalid sort_by '{sort_by}'. Allowed: {valid_fields}"}
    if order not in valid_orders:
        return {"error": f"Invalid order '{order}'. Allowed: {valid_orders}"}

    reverse = order == "desc"
    sorted_list = sorted(
        books, key=lambda b: b[sort_by].lower(), reverse=reverse
    )
    return {
        "sort_by": sort_by,
        "order": order,
        "total": len(sorted_list),
        "books": sorted_list,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q18 — GET /books/page  (pagination)                             Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/page")
def paginate_books(
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=3, gt=0),
):
    total = len(books)
    total_pages = math.ceil(total / limit) if total > 0 else 1
    start = (page - 1) * limit
    end = start + limit
    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "books": books[start:end],
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q20 — GET /books/browse  (search + sort + pagination combined)  Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/browse")
def browse_books(
    keyword: Optional[str] = None,
    sort_by: str = Query(default="title"),
    order: str = Query(default="asc"),
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=3, gt=0),
):
    valid_fields = ["title", "author", "genre"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        return {"error": f"Invalid sort_by. Allowed: {valid_fields}"}
    if order not in valid_orders:
        return {"error": f"Invalid order. Allowed: {valid_orders}"}

    # Step 1 — Filter by keyword
    if keyword is not None:
        kw = keyword.lower()
        results = [
            b
            for b in books
            if kw in b["title"].lower() or kw in b["author"].lower()
        ]
    else:
        results = books.copy()

    # Step 2 — Sort
    results = sorted(
        results,
        key=lambda b: b[sort_by].lower(),
        reverse=(order == "desc"),
    )

    # Step 3 — Paginate
    total = len(results)
    total_pages = math.ceil(total / limit) if total > 0 else 1
    start = (page - 1) * limit
    paginated = results[start : start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "current_page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "books": paginated,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q3 — GET /books/{book_id}  (AFTER all fixed /books/* routes)    Day 1
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    book = find_book(book_id)
    if book is None:
        return {"error": "Book not found"}
    return book


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q11 — POST /books  (add new book, 201, duplicate check)         Day 4
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.post("/books", status_code=201)
def add_book(new_book: NewBook):
    # Reject duplicate titles (case-insensitive)
    for book in books:
        if book["title"].lower() == new_book.title.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Book with title '{new_book.title}' already exists",
            )

    new_id = max(b["id"] for b in books) + 1 if books else 1
    book_dict = {
        "id": new_id,
        "title": new_book.title,
        "author": new_book.author,
        "genre": new_book.genre,
        "is_available": new_book.is_available,
    }
    books.append(book_dict)
    return {"message": "Book added successfully", "book": book_dict}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q12 — PUT /books/{book_id}  (update, 404 if missing)            Day 4
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    genre: Optional[str] = None,
    is_available: Optional[bool] = None,
):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if genre is not None:
        book["genre"] = genre
    if is_available is not None:
        book["is_available"] = is_available

    return {"message": "Book updated successfully", "book": book}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q13 — DELETE /books/{book_id}  (404 if missing)                 Day 4
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    books.remove(book)
    return {"message": f"Book '{book['title']}' deleted successfully"}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q19 — GET /borrow-records/search  (FIXED route — before vars)   Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/borrow-records/search")
def search_borrow_records(member_name: str = Query(..., min_length=1)):
    kw = member_name.lower()
    results = [r for r in borrow_records if kw in r["member_name"].lower()]
    if not results:
        return {
            "message": f"No borrow records found for '{member_name}'",
            "total_found": 0,
            "results": [],
        }
    return {
        "keyword": member_name,
        "total_found": len(results),
        "results": results,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q19 — GET /borrow-records/page  (pagination for records)        Day 6
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/borrow-records/page")
def paginate_borrow_records(
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=3, gt=0),
):
    total = len(borrow_records)
    total_pages = math.ceil(total / limit) if total > 0 else 1
    start = (page - 1) * limit
    paginated = borrow_records[start : start + limit]
    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "records": paginated,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q4 — GET /borrow-records  (all records + count)                 Day 1
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.get("/borrow-records")
def get_borrow_records():
    return {"total": len(borrow_records), "records": borrow_records}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q8 — POST /borrow  (uses helpers, creates record)        Day 2 + Day 3
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.post("/borrow")
def borrow_book(request: BorrowRequest):
    global record_counter

    # Use helper to find book
    book = find_book(request.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book['title']}' is already borrowed",
        )

    # Q9: Enforce borrow-day limits per member type
    if request.member_type != "premium" and request.borrow_days > 30:
        raise HTTPException(
            status_code=400,
            detail="Regular members can borrow for a maximum of 30 days. "
            "Upgrade to premium for up to 60 days.",
        )

    # Use helper for due date
    due_date = calculate_due_date(request.borrow_days, request.member_type)

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": request.member_name,
        "member_id": request.member_id,
        "member_type": request.member_type,
        "book_id": request.book_id,
        "book_title": book["title"],
        "borrow_days": request.borrow_days,
        "due_date": due_date,
    }
    borrow_records.append(record)
    record_counter += 1

    return {"message": "Book borrowed successfully", "record": record}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q14 — POST /queue/add  +  GET /queue   (waitlist)               Day 5
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.post("/queue/add")
def add_to_queue(
    member_name: str = Query(..., min_length=2),
    book_id: int = Query(..., gt=0),
):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book['title']}' is currently available — "
            "borrow it directly instead of queuing!",
        )

    queue_entry = {
        "member_name": member_name,
        "book_id": book_id,
        "book_title": book["title"],
    }
    queue.append(queue_entry)
    return {
        "message": f"'{member_name}' added to waitlist for '{book['title']}'",
        "queue_entry": queue_entry,
    }


@app.get("/queue")
def get_queue():
    return {"total_in_queue": len(queue), "queue": queue}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Q15 — POST /return/{book_id}  (return + auto-reassign)          Day 5
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.post("/return/{book_id}")
def return_book(book_id: int):
    global record_counter

    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book['title']}' is not currently borrowed",
        )

    book["is_available"] = True

    # Check queue — auto-assign to first person waiting for this book
    waiting = None
    for entry in queue:
        if entry["book_id"] == book_id:
            waiting = entry
            break

    if waiting:
        queue.remove(waiting)
        book["is_available"] = False

        due_date = calculate_due_date(14, "regular")
        record = {
            "record_id": record_counter,
            "member_name": waiting["member_name"],
            "member_id": "AUTO-ASSIGNED",
            "member_type": "regular",
            "book_id": book_id,
            "book_title": book["title"],
            "borrow_days": 14,
            "due_date": due_date,
        }
        borrow_records.append(record)
        record_counter += 1

        return {
            "message": f"Book returned and re-assigned to "
            f"'{waiting['member_name']}'",
            "new_borrow_record": record,
        }

    return {
        "message": f"Book '{book['title']}' returned successfully "
        "and is now available"
    }
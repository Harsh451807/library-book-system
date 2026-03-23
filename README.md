# 📚 Library Book System — FastAPI Backend

A complete Library Book Management System built with **FastAPI**, 
featuring 20 API endpoints covering CRUD operations, multi-step 
workflows, search, sorting, and pagination.

## 🚀 Tech Stack
- **FastAPI** — Python web framework
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

## 📋 Features Implemented
| Day | Concept | Status |
|-----|---------|--------|
| Day 1 | GET Endpoints + JSON responses | ✅ |
| Day 2 | POST + Pydantic validation | ✅ |
| Day 3 | Helper functions + Filters | ✅ |
| Day 4 | CRUD — Create, Update, Delete | ✅ |
| Day 5 | Multi-step workflow (Queue + Return) | ✅ |
| Day 6 | Search, Sort, Pagination | ✅ |

## 🔗 API Endpoints (20 Total)
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | GET | `/` | Welcome message |
| 2 | GET | `/books` | All books with counts |
| 3 | GET | `/books/{book_id}` | Single book by ID |
| 4 | GET | `/borrow-records` | All borrow records |
| 5 | GET | `/books/summary` | Stats + genre breakdown |
| 6-8 | POST | `/borrow` | Borrow with Pydantic validation |
| 9 | POST | `/borrow` | Premium member support |
| 10 | GET | `/books/filter` | Filter by genre/author/available |
| 11 | POST | `/books` | Add new book (201) |
| 12 | PUT | `/books/{book_id}` | Update book |
| 13 | DELETE | `/books/{book_id}` | Delete book |
| 14 | POST/GET | `/queue/add`, `/queue` | Waitlist system |
| 15 | POST | `/return/{book_id}` | Return + auto-reassign |
| 16 | GET | `/books/search` | Keyword search |
| 17 | GET | `/books/sort` | Sort by field |
| 18 | GET | `/books/page` | Pagination |
| 19 | GET | `/borrow-records/search` | Search records |
| 20 | GET | `/books/browse` | Combined search+sort+page |

## 🖥️ How to Run
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# Open http://127.0.0.1:8000/docs

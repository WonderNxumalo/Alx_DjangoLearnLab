# Advanced API Project: Book Endpoints

This document outlines the API endpoints configured for the `Book` model.

## API Endpoints

All endpoints are accessible under the base URL `/api/`.

| Endpoint Path | HTTP Method | View Class | Functionality | Permissions |
| :--- | :--- | :--- | :--- | :--- |
| `/api/books/` | **GET** | `BookListCreateAPIView` | **List** all books. | Allowed for all users. |
| `/api/books/` | **POST** | `BookListCreateAPIView` | **Create** a new book. | Allowed for all users. |
| `/api/books/<int:pk>/` | **GET** | `BookRetrieveUpdateDestroyAPIView` | **Retrieve** a single book. | Allowed for all users. |
| `/api/books/<int:pk>/` | **PUT/PATCH** | `BookRetrieveUpdateDestroyAPIView` | **Update** an existing book. | **Restricted to authenticated users.** |
| `/api/books/<int:pk>/` | **DELETE** | `BookRetrieveUpdateDestroyAPIView` | **Delete** a book. | **Restricted to authenticated users.** |

## Custom Settings/Hooks

### 1. Permission Enforcement

The views use the custom `IsAuthenticatedOrCreateOnly` permission class, which extends `permissions.BasePermission`.

* **Logic:** It allows `GET`, `HEAD`, `OPTIONS`, and `POST` (safe methods plus create) for all users.
* **Restriction:** It restricts dangerous methods (`PUT`, `PATCH`, `DELETE`) to users who are currently authenticated (`request.user.is_authenticated`).

### 2. Data Validation

The creation and update views (`ListCreateAPIView` and `RetrieveUpdateDestroyAPIView`) automatically trigger the custom `validate_publication_year` method defined in the `BookSerializer` to prevent future years from being saved.
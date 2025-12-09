A Social Media API using Django and Django REST Framework (DRF).

This project covers key aspects of building a robust API, including setting up the project, implementing user authentication, adding core functionalities such as posts, comments, follows, and notifications, and finally deploying the API to a production environment.

# Post and Comment Documentation

Endpoint URLs: The full paths, e.g., POST /api/posts/

Authentication: Requires Authorization: Token <token>

Request/Response Examples:

Example Request (POST /api/posts/):

JSON
{
    "title": "My First Post",
    "content": "This is content of the post."
}
Example Response (Success 201):

JSON
{
    "id": 1,
    "title": "My First Post",
    "content": "This is content of the post.",
    "author_info": { /* ... user details ... */ },
    "comment_count": 0,
    // ... timestamps ...
}

# Follow and Unfollow Documentation

Feature	Endpoint URL	Method	Authentication	Description
Follow User	/accounts/follow/<int:user_pk>/	POST	Required	Adds the target user (user_pk) to the authenticated user's following list.
Unfollow User	/accounts/unfollow/<int:user_pk>/	POST	Required	Removes the target user (user_pk) from the authenticated user's following list.
User Feed	/api/feed/	GET	Required	Returns a paginated list of posts from all users the authenticated user is following.

# Like and Unlike Notifications' Documentation

Feature	Endpoint URL	Method	Auth	Description
Like/Unlike Post	/api/posts/<int:pk>/like/	POST	Required	Toggles the like status on a post. Creates a Notification if a new like is registered.
Fetch Notifications	/notifications/	GET	Required	Retrieves the authenticated user's notifications. Displays the unread_count and marks displayed notifications as read.
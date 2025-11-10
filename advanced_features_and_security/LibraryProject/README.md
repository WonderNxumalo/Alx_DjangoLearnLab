Duplicated folder to create django-models for the relationship_app


Django Permissions and Group Setup

This document outlines how custom permissions and Django Groups are configured and used within the relationship_app to restrict access to book management functionalities.

1. Custom Model Permissions (Defined in relationship_app/models.py)

Custom permissions are defined on the Book model within its Meta class. These permissions are the granular access controls used across the application:

relationship_app.can_view: Allows a user to view the book list and details.

relationship_app.can_create: Allows a user to add a new book.

relationship_app.can_edit: Allows a user to modify an existing book.

relationship_app.can_delete: Allows a user to remove a book.

2. Group Configuration (Managed via Django Admin)

To simplify user management, these custom permissions are assigned to specific groups using the Django Admin interface.

Group Name

Assigned Permissions

Role

Viewers

can_view

Standard user/member who can only browse the catalog.

Editors

can_view, can_create, can_edit

Librarians or content managers who can add and modify books.

Admins

All permissions: can_view, can_create, can_edit, can_delete

Superusers or high-level admins with full control, including deletion.

Note: The actual creation and assignment of permissions to these groups is done manually by a Superuser through the Django admin interface after running migrations.

3. Enforcement in Views (Implemented in relationship_app/views.py)

Access control is enforced using the built-in @permission_required decorator from django.contrib.auth.decorators.

View Function

Required Permission

book_add

relationship_app.can_create

book_edit

relationship_app.can_edit

book_delete

relationship_app.can_delete

This system ensures that only users belonging to a Group that has been assigned the specific permission can access the secured view logic.

Security Best Practices Implementation

We have implemented several security enhancements to protect the application against common vulnerabilities.

4. Secure Settings Configuration (settings.py)

The following configurations have been set to enhance browser and network-level security:

DEBUG = False: Ensures that sensitive application and server information is not exposed to users in a production environment.

X_FRAME_OPTIONS = 'DENY': Protects against Clickjacking attacks by preventing the site from being embedded in a frame.

SECURE_CONTENT_TYPE_NOSNIFF = True: Prevents the browser from attempting to guess the content type, mitigating some forms of XSS attacks.

SESSION_COOKIE_SECURE = True and CSRF_COOKIE_SECURE = True: Ensures that session and CSRF tokens are only transmitted over secure (HTTPS) connections.

SESSION_COOKIE_HTTPONLY = True and CSRF_COOKIE_HTTPONLY = True: Prevents client-side scripts (JavaScript) from accessing these cookies, protecting against cookie theft via XSS.

5. Cross-Site Request Forgery (CSRF) Protection

All interactive forms (login and registration) have been updated to explicitly include the {% csrf_token %} template tag. This mandatory token ensures that form submissions are only accepted from requests originating from our application, providing protection against CSRF attacks.

6. SQL Injection and XSS Mitigation

SQL Injection: The application uses the Django ORM exclusively (Book.objects.all(), etc.). The ORM parameterizes all database queries, making the application inherently resilient to SQL Injection attacks. No direct raw SQL queries are used.

XSS (Cross-Site Scripting): Django templates automatically escape output by default. This means user-provided data rendered in HTML is safely converted to its plain text equivalent, preventing malicious scripts from executing and mitigating XSS vulnerabilities.
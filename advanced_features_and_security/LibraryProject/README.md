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

=== Deployment Config for HTTPS

Deployment Configuration: Enforcing HTTPS

This document outlines the necessary steps to configure your web server (Nginx or Apache) to support HTTPS (SSL/TLS) and ensure secure communication, complementing the Django settings configured in settings.py.

Step 1: Obtain an SSL/TLS Certificate

Before configuring the server, you must have a valid certificate for your domain (e.g., from Let's Encrypt, which is free).

Files Required:

your_domain.crt (Certificate file)

your_domain.key (Private key file)

chain.crt (Intermediate certificate/chain)

Step 2: Configure HTTPS on the Web Server

A. Nginx Configuration Example

Modify your Nginx server block configuration (e.g., in /etc/nginx/sites-available/your_site.conf).

server {
    # 1. HTTP to HTTPS Redirect
    listen 80;
    server_name yourdomain.com [www.yourdomain.com](https://www.yourdomain.com);
    return 301 https://$host$request_uri;
}

server {
    # 2. HTTPS Listener
    listen 443 ssl http2;
    server_name yourdomain.com [www.yourdomain.com](https://www.yourdomain.com);

    # SSL/TLS Certificate Paths
    ssl_certificate /etc/letsencrypt/live/[yourdomain.com/fullchain.pem](https://yourdomain.com/fullchain.pem);
    ssl_certificate_key /etc/letsencrypt/live/[yourdomain.com/privkey.pem](https://yourdomain.com/privkey.pem);

    # Optional: Stronger Security Configuration (Recommended)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    # ... more cipher settings

    # Proxy traffic to the Django application (e.g., Gunicorn/uWSGI)
    location / {
        proxy_pass http://unix:/path/to/your/gunicorn.sock;
        # ... other proxy headers
    }
}


B. Apache Configuration Example

Modify your Apache VirtualHost configuration (e.g., in /etc/apache2/sites-available/your_site-le-ssl.conf).

<VirtualHost *:80>
    ServerName yourdomain.com
    # 1. HTTP to HTTPS Redirect
    Redirect permanent / [https://yourdomain.com/](https://yourdomain.com/)
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yourdomain.com

    # SSL/TLS Certificate Paths
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/[yourdomain.com/fullchain.pem](https://yourdomain.com/fullchain.pem)
    SSLCertificateKeyFile /etc/letsencrypt/live/[yourdomain.com/privkey.pem](https://yourdomain.com/privkey.pem)

    # Proxy traffic to the Django application (e.g., mod_wsgi)
    # ... WSGI/Proxy configuration here
</VirtualHost>
</IfModule>


Step 3: Apply Changes

Test your web server configuration for syntax errors.

Reload or restart the web server (e.g., sudo systemctl reload nginx or sudo systemctl reload apache2).

The Django settings (SECURE_SSL_REDIRECT = True, HSTS) will now be effective, ensuring all traffic is secured via HTTPS.

=== Security Measures & Review ===

Security Measures and Review Report

This report summarizes the security enhancements implemented in the Django application to mitigate common web vulnerabilities and enforce secure communication standards.

1. HTTPS Enforcement and Transport Security

Configuration

Setting

Contribution to Security

SECURE_SSL_REDIRECT

True

Automatically redirects all incoming HTTP requests to HTTPS, ensuring all data transmission is encrypted from the start.

SECURE_HSTS_SECONDS

1 Year (31536000)

Implements HTTP Strict Transport Security (HSTS), instructing supporting browsers to only communicate with the site via HTTPS for the specified duration.

SECURE_HSTS_PRELOAD

True

Allows the domain to be added to browser HSTS preload lists for maximum protection against downgrade attacks.

Web Server Config

Nginx/Apache 301 Redirect

Configured the external web server to listen on port 80 and immediately redirect to 443.

2. Cookie and Session Security

Configuration

Setting

Vulnerability Mitigated

SESSION_COOKIE_SECURE

True

Ensures session cookies are only sent over encrypted (HTTPS) channels.

CSRF_COOKIE_SECURE

True

Ensures CSRF cookies are only sent over encrypted (HTTPS) channels.

SESSION_COOKIE_HTTPONLY

True

Prevents client-side scripts (JavaScript) from accessing the session cookie, protecting against cookie theft via Cross-Site Scripting (XSS).

CSRF_COOKIE_HTTPONLY

True

Prevents client-side scripts from accessing the CSRF cookie.

3. Browser/Header Protection

Configuration

Setting

Vulnerability Mitigated

X_FRAME_OPTIONS

'DENY'

Protection against Clickjacking by preventing the site from being embedded in an iframe.

SECURE_CONTENT_TYPE_NOSNIFF

True

Mitigates mime-type confusion attacks, reducing the risk of file-based XSS.

SECURE_BROWSER_XSS_FILTER

True

Activates built-in browser XSS protection mechanisms.

4. Application-Level Mitigations

Area

Strategy Implemented

Vulnerability Mitigated

Forms

Explicit {% csrf_token %} in all forms.

Cross-Site Request Forgery (CSRF).

Database

Exclusive use of Django ORM.

SQL Injection (ORM parameterizes queries automatically).

Templates

Django's default auto-escaping for output.

Cross-Site Scripting (XSS) (User data is rendered as plain text).

Permissions

@permission_required decorators on views.

Unauthorized access to CRUD operations based on user role and group.

Areas for Potential Improvement

Content Security Policy (CSP): While Django's default escaping is strong, implementing a strict CSP header (using django-csp or similar) is the next level of defense against XSS, explicitly controlling which sources (scripts, styles) the browser can load.

Rate Limiting: Implementing rate limiting on high-traffic or resource-intensive endpoints (like login/registration) would protect against denial-of-service (DoS) and brute-force attacks.

Third-Party Dependencies: A regular audit of all external Python and JavaScript libraries is necessary to ensure they do not introduce known vulnerabilities.
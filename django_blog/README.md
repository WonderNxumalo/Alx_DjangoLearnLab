Authentication Documentation

The authentication system relies on a combination of built-in Django features and custom implementation.

Core Components:

User Model: The default django.contrib.auth.models.User is used, ensuring industry-standard password hashing (PBKDF2).

Registration (/register/):

Uses the custom RegisterView (a CreateView).

The CustomUserCreationForm extends the default form to explicitly include the email field.

Login/Logout:

Handled by Django's built-in LoginView and LogoutView, accessed via the path('accounts/', include('django.contrib.auth.urls')) setup in the project's urls.py.

Profile Management (/profile/):

Uses a custom profile_view function secured with the @login_required decorator.

Allows authenticated users to update their email address using the UserProfileForm.
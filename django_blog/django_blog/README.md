Authentication System Documentation

The project uses a hybrid authentication system combining Django's robust built-in views and custom components for tailored functionality.

Authentication Process

Component	Functionality	Implementation Details
Registration (/register/)	Allows new user account creation.	Handled by the RegisterView (a custom Django CreateView). It uses the CustomUserCreationForm to ensure the email field is collected.
Login/Logout	Standard user session management.	Handled by Django's built-in views via the path('accounts/', include('django.contrib.auth.urls')) setting. The named URLs like login and logout are automatically available.
Profile Management (/profile/)	Allows authenticated users to update details.	Handled by the custom function profile_view, which is secured with the @login_required decorator. It uses the UserProfileForm to update the user's email.
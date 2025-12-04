Authentication System Documentation

The project uses a hybrid authentication system combining Django's robust built-in views and custom components for tailored functionality.

Authentication Process

Component	Functionality	Implementation Details
Registration (/register/)	Allows new user account creation.	Handled by the RegisterView (a custom Django CreateView). It uses the CustomUserCreationForm to ensure the email field is collected.
Login/Logout	Standard user session management.	Handled by Django's built-in views via the path('accounts/', include('django.contrib.auth.urls')) setting. The named URLs like login and logout are automatically available.
Profile Management (/profile/)	Allows authenticated users to update details.	Handled by the custom function profile_view, which is secured with the @login_required decorator. It uses the UserProfileForm to update the user's email.

=== Comment Views ===

The comment feature provides full CRUD functionality for authenticated users on individual blog posts.

Model: The Comment model is linked to Post and User via foreign keys. It includes content, created_at, and updated_at fields.

Visibility: Comments are visible to all users (authenticated or not) via the PostDetailView template.

Permissions:

Creation: Requires authentication (LoginRequiredMixin). The comment is automatically associated with the post based on the URL and the author based on the session user.

Edit/Delete: Requires the user to be the exact author of the comment (LoginRequiredMixin + UserPassesTestMixin). Unauthorized users are blocked with a 403 error.

URLs: Comment actions are logically nested. Creation uses the post's primary key (/posts/<post_pk>/comment/new/), while update and delete use the comment's primary key (/comment/<pk>/edit/).

=== Tagging and Search Feature ===

This system utilizes django-taggit and custom Django logic for improved content organization and discovery.

I. Tagging Integration

Model: The Post model includes a tags = TaggableManager() field, providing a simple way to attach multiple tags to a single post.

Form: The PostForm includes the tags field, allowing users to enter comma-separated tags during creation or editing.

Discovery:

Tagged List: The view tagged_posts_list handles the URL pattern /tags/<slug:tag_slug>/, filtering posts to display only those associated with the requested tag.

Template Links: Tag links in the detail and list views use {% url 'tagged_posts' tag_slug=tag.slug %} to direct users to the filtered list.

II. Search Functionality

Implementation: The search_results view processes queries submitted via the search form in base.html.

Search Criteria: Search is complex and efficient, using Django's Q objects to query posts based on:

Content within the title (title__icontains).

Content within the content body (content__icontains).

Posts associated with an exact tag name match (using the taggit.models.Tag model).

User Guide: Users can enter any keyword into the search bar, and the system will return posts where the keyword appears in the title, content, or as a tag.
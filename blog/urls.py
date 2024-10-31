from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="post_list"),
    path('posts/<int:id>', views.post_detail, name="post_detail"),
    path('posts/<post_id>/comment', views.post_comment, name="post_comment"),
    path('ticket', views.ticket, name='ticket'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_post', views.create_post, name="create_post"),
    path('profile/delete_post/<post_id>', views.delete_post, name="delete_post"),
    path('profile/edit_post/<post_id>', views.edit_post, name="edit_post"),
    path('profile/delete_image/<image_id>', views.delete_image, name="delete_image"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password_reset/complete'),
         name="password_reset_confirm"),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/', views.register, name='register'),
    path('account/edit', views.edit_account, name='edit_account'),
    path('account_detail/<account_id>', views.account_detail, name="account_detail"),
    path('profile/comments', views.user_comments, name="user_comments")
]

from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Book URLs
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/add/', views.BookCreateView.as_view(), name='book-add'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book-edit'),
    
    # Member URLs
    path('members/', views.MemberListView.as_view(), name='member-list'),
    path('members/add/', views.MemberCreateView.as_view(), name='member-add'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member-edit'),
    
    # Book Issue URLs
    path('issue-book/', views.IssueBookView.as_view(), name='issue-book'),
    path('return-book/<int:issue_id>/', views.return_book, name='return-book'),
]
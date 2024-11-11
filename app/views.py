from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.utils import timezone
from .models import Book, Member, BookIssue
from django.contrib.auth import logout

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        context['total_members'] = Member.objects.count()
        context['books_issued'] = BookIssue.objects.filter(is_returned=False).count()
        context['total_fines'] = BookIssue.objects.aggregate(total=Sum('fine_amount'))['total'] or 0
        
        # Recent books (last 5 added)
        context['recent_books'] = Book.objects.order_by('-added_date')[:5]
        
        # Recent issues (last 5 issues)
        context['recent_issues'] = BookIssue.objects.order_by('-issue_date')[:5]
        
        return context

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'app/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search filter
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query)
            )
        
        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category = self.request.GET.get('category', '')
        
        # Get categories with their display names (including fixed count)
        categories = []
        for code, name in Book.CATEGORY_CHOICES:
            categories.append((code, name, code == current_category))
        
        context['categories'] = categories
        context['current_category'] = current_category
        context['search_query'] = self.request.GET.get('q', '')
        
        # Get current category name
        if current_category:
            category_dict = dict(Book.CATEGORY_CHOICES)
            context['current_category_name'] = category_dict.get(current_category, 'Unknown').split(':')[0]
        
        return context

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'app/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue_history'] = BookIssue.objects.filter(book=self.object)
        context['now'] = timezone.now()
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'app/book_form.html'
    fields = ['title', 'isbn', 'author', 'category', 'description', 'publisher', 'publication_year', 'edition']
    success_url = reverse_lazy('app:book-list')

    def form_valid(self, form):
        messages.success(self.request, 'Book added successfully.')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'app/book_form.html'
    fields = ['title', 'isbn', 'author', 'category', 'status', 'description', 'publisher', 'publication_year', 'edition']
    success_url = reverse_lazy('app:book-list')

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully.')
        return super().form_valid(form)

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'app/member_list.html'
    context_object_name = 'members'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Member.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).order_by('name')
        return Member.objects.all().order_by('name')

class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'app/member_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_books'] = BookIssue.objects.filter(
            member=self.object,
            is_returned=False
        )
        context['issue_history'] = BookIssue.objects.filter(
            member=self.object
        ).order_by('-issue_date')
        context['now'] = timezone.now()
        return context

class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    template_name = 'app/member_form.html'
    fields = ['name', 'email', 'phone', 'address']
    success_url = reverse_lazy('app:member-list')

    def form_valid(self, form):
        messages.success(self.request, 'Member added successfully.')
        return super().form_valid(form)

class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'app/member_form.html'
    fields = ['name', 'email', 'phone', 'address', 'status']
    success_url = reverse_lazy('app:member-list')

    def form_valid(self, form):
        messages.success(self.request, 'Member updated successfully.')
        return super().form_valid(form)

class IssueBookView(LoginRequiredMixin, CreateView):
    model = BookIssue
    template_name = 'app/issue_book_form.html'
    fields = ['book', 'member', 'due_date']
    success_url = reverse_lazy('app:dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show available books
        form.fields['book'].queryset = Book.objects.filter(status='AVAILABLE')
        # Only show active members
        form.fields['member'].queryset = Member.objects.filter(status='ACTIVE')
        return form

    def form_valid(self, form):
        book = form.cleaned_data['book']
        if book.status == 'ISSUED':
            messages.error(self.request, 'This book is already issued.')
            return self.form_invalid(form)
        
        book.status = 'ISSUED'
        book.save()
        messages.success(self.request, 'Book issued successfully.')
        return super().form_valid(form)

def return_book(request, issue_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    book_issue = get_object_or_404(BookIssue, id=issue_id)
    if not book_issue.is_returned:
        book_issue.is_returned = True
        book_issue.return_date = timezone.now()
        book_issue.calculate_fine()
        book_issue.save()
        
        book = book_issue.book
        book.status = 'AVAILABLE'
        book.save()
        
        messages.success(request, 'Book returned successfully.')
    return redirect('app:dashboard')

def logoutview(request):
    logout(request)
    return redirect("/library")
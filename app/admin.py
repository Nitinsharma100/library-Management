from django.contrib import admin
from .models import Book, Member, BookIssue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'category', 'status', 'added_date')
    list_filter = ('status', 'category')
    search_fields = ('title', 'isbn', 'author')
    ordering = ('-added_date',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'membership_date', 'total_fines')
    list_filter = ('status', 'membership_date')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-membership_date',)

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'return_date', 'is_returned', 'fine_amount')
    list_filter = ('is_returned', 'issue_date')
    search_fields = ('book__title', 'member__name')
    ordering = ('-issue_date',)
    
    def save_model(self, request, obj, form, change):
        if obj.is_returned and not obj.return_date:
            obj.return_date = timezone.now()
        super().save_model(request, obj, form, change)
        
    actions = ['calculate_fines']
    
    def calculate_fines(self, request, queryset):
        for book_issue in queryset:
            book_issue.calculate_fine()
        self.message_user(request, f"Fines calculated for {queryset.count()} book issues.")
    calculate_fines.short_description = "Calculate fines for selected book issues"
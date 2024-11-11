from django.db import models
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('BUSINESS', 'BUSINESS: 5'),
        ('SCIENCE', 'SCIENCE: 5'),
        ('COMPUTER', 'COMPUTER: 5'),
        ('MATHEMATICS', 'MATHEMATICS: 5'),
        ('PHYSICS', 'PHYSICS: 5'),
        ('CHEMISTRY', 'CHEMISTRY: 5'),
        ('BIOLOGY', 'BIOLOGY: 5'),
        ('ECONOMICS', 'ECONOMICS: 5'),
        ('MANAGEMENT', 'MANAGEMENT: 5'),
        ('MARKETING', 'MARKETING: 5'),
        ('FINANCE', 'FINANCE: 5'),
        ('LITERATURE', 'LITERATURE: 5'),
        ('HISTORY', 'HISTORY: 5'),
        ('PHILOSOPHY', 'PHILOSOPHY: 5'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ISSUED', 'Issued'),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    added_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def get_category_display_with_count(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class Member(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    total_fines = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f"{self.name} ({self.email})"

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Book Issue'
        verbose_name_plural = 'Book Issues'

    def save(self, *args, **kwargs):
        if not self.due_date:
            # Set due date to 14 days from issue date by default
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    def calculate_fine(self):
        if self.is_returned and self.return_date > self.due_date:
            # Calculate fine: $1 per day overdue
            days_overdue = (self.return_date - self.due_date).days
            self.fine_amount = max(0, days_overdue * 1.00)
            self.save()
        return self.fine_amount

    def __str__(self):
        return f"{self.book.title} - {self.member.name} ({self.issue_date.date()})"
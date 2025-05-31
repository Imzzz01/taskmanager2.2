from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
        
    @property
    def is_overdue(self):
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False

# Subcription models

class SubscriptionPlan(models.Model):
    PLAN_TYPES = (
        ('free', 'Free'),
          ('basic', 'Basic'),
        ('premium', 'Premium'),  
    )

    name = models.CharField(max_length=50, choices=PLAN_TYPES, unique=True)
    display_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_tasks = models.IntegerField() 
    max_categories = models.IntegerField()
    description = models.TextField()
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

        class Meta:
            ordering ['price']

class UserSubscription(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

user = models.OnetoOneField(User, on_delete=models.CASCADE, related_name='subscription')   
plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
start_date = models.DateTimeField(auto_now_add=True)
end_date = models.DateTimeField()
status = models.CharField(max_length=10, choices=status_choices, default='active')
auto_renew = models.BooleanField(default=True)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.display_name}"

    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

@property
def days_remaining(self):
    if self.is_active:
        return (self.end_date - timezone.now()).days
    return 0

def can_create_task(self):
    if self.is_active:
        return self.user.task_set.count() < self.plan.max_tasks
    return False
    current_tasks = Task.objects.filter(user=self.user, completed=False).count()
    return current_tasks < self.plan.max_tasks

def can_create_category(self):
    if self.is_active:
        return self.user.category_set.count() < self.plan.max_categories
    return False
    current_categories = Category.objects.filter(user=self.user).count()
    return current_categories < self.plan.max_categories

class Cart(models.Model):
    user = models.OnetoOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return f"Cart for {self.user.username}"

@property 
def total_amount(self):
    return sum(item.plan.price for item in self.items.all())

@property
def total_items(self):
    
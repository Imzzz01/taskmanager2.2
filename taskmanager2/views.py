
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task, Category
from .forms import TaskForm, CategoryForm
from django.contrib.auth import views as auth_views

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    categories = Category.objects.filter(user=request.user)
    category_form = CategoryForm()

    priority = request.GET.get('priority', '')
    category_id = request.GET.get('category', '')
    search_query = request.GET.get('search', '')  # Changed variable name

    if priority:
        tasks = tasks.filter(priority=priority)
    if category_id:
        tasks = tasks.filter(category_id=category_id)
    if search_query: # Apply the filter
        tasks = tasks.filter(title__icontains=search_query)

    context = {
        'tasks': tasks,
        'categories': categories,
        'category_form': category_form,
        'current_priority': priority,
        'current_category': category_id,
        'current_search': search_query, 
    }
    return render(request, 'taskmanager2/dashboard.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm(request.user)
    
    return render(request, 'taskmanager2/task_form.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(request.user, instance=task)
    
    return render(request, 'taskmanager2/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'taskmanager2/confirm_delete.html', {'task': task})

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

@login_required
@require_POST
def add_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        return JsonResponse({
            'success': True,
            'category_id': category.id,
            'category_name': category.name
        })
    return JsonResponse({'success': False})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'taskmanager2/category_form.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('dashboard')
    return render(request, 'taskmanager2/confirm_delete.html', {'category': category})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Change to your desired redirect
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
  
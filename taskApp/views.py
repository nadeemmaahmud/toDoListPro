from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Category, Task
from . forms import TaskCreateEditForm, CategoryCreateEditForm

@login_required
def todo(request):
    tasks = Task.objects.filter(is_complete=False, user=request.user)
    return render(request, 'task/todo.html', {'tasks': tasks})

@login_required
def completed(request):
    tasks = Task.objects.filter(is_complete=True, user=request.user)
    return render(request, 'task/completed.html', {'tasks': tasks})

@login_required
def all(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task/all.html', {'tasks': tasks})

@login_required
def create(request):
    if request.method == 'POST':
        form = TaskCreateEditForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully...")
            return redirect('todo')
    else:
        form = TaskCreateEditForm()

    return render(request, 'task/create_edit_task.html', {'form': form, 'create': True})

@login_required
def edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskCreateEditForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' edited successfully...")
            return redirect('todo')
    else:
        form = TaskCreateEditForm(instance=task)

    return render(request, 'task/create_edit_task.html', {'form': form})

@login_required
def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, f"Task '{task.title}' deleted successfully...")
        return redirect('todo')

    return render(request, 'task/delete.html', {'task': task})

@login_required
def complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.is_complete = True
        task.save()
        messages.success(request, f"Task '{task.title}' completed successfully...")
        return redirect('todo')

    return render(request, 'task/complete.html', {'task': task})

@login_required
def all_category(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'task/all_category.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryCreateEditForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f"Category '{category}' created successfully...")
            return redirect('all_category')
    else:
        form = CategoryCreateEditForm()

    return render(request, 'task/add_edit_category.html', {'form': form, 'add': True})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryCreateEditForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category}' edited successfully...")
            return redirect('all_category')
    else:
        form = CategoryCreateEditForm(instance=category)

    return render(request, 'task/add_edit_category.html', {'form': form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, f"Category '{category}' deleted successfully...")
        return redirect('all_category')

    return render(request, 'task/delete.html', {'category': category, 'delete_category': True})

@login_required
def search_task(request):
    query = request.GET.get('q', '')
    user = request.user

    tasks = Task.objects.filter(user=user)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'task/search_results.html', {'tasks': tasks, 'query': query})
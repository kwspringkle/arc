from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, SearchForm

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    search_form = SearchForm(request.GET)
    if search_form.is_valid() and 'query' in request.GET:
        query = search_form.cleaned_data['query']
        if query:
            posts = posts.filter(content__icontains=query)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'posts/index.html', {'posts': posts, 'form': form, 'search_form': search_form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('index')
    return render(request, 'posts/confirm_delete.html', {'post': post})

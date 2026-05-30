from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import FarmPost, PostLike, PostComment


@login_required
def create_post_view(request):
    if not request.user.is_seller:
        messages.error(request, 'Only sellers can create posts.')
        return redirect('home')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        if content:
            FarmPost.objects.create(seller=request.user, content=content, image=image)
            messages.success(request, 'Post created.')
        else:
            messages.error(request, 'Post content cannot be empty.')
    return redirect('farms:my_farm')


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(FarmPost, pk=pk, seller=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('farms:my_farm')


@login_required
def like_post_view(request, pk):
    post = get_object_or_404(FarmPost, pk=pk)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.get_like_count()})


@login_required
def add_comment_view(request, pk):
    post = get_object_or_404(FarmPost, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            comment = PostComment.objects.create(post=post, user=request.user, comment=comment_text)
            return JsonResponse({
                'success': True,
                'user': request.user.full_name,
                'comment': comment.comment,
                'created_at': comment.created_at.strftime('%b %d, %Y'),
                'count': post.get_comment_count(),
            })
    return JsonResponse({'success': False})


def feed_view(request):
    posts = FarmPost.objects.select_related('seller__farm_profile').all()
    return render(request, 'social/feed.html', {'posts': posts})

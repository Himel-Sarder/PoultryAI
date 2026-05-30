from django import template

register = template.Library()

@register.filter
def is_liked_by(post, user):
    if not user or not user.is_authenticated:
        return False
    return post.likes.filter(user=user).exists()

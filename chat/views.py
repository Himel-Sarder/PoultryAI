from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import ChatMessage, get_ai_response
from accounts.models import User


@login_required
def chat_list_view(request):
    # Get unique conversations
    user = request.user
    conversations = []
    contacts = User.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()

    for contact in contacts:
        last_msg = ChatMessage.objects.filter(
            Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user)
        ).last()
        unread = ChatMessage.objects.filter(sender=contact, receiver=user, is_read=False).count()
        conversations.append({
            'contact': contact,
            'last_message': last_msg,
            'unread': unread,
        })
    return render(request, 'chat/chat_list.html', {'conversations': conversations})


@login_required
def chat_detail_view(request, user_id):
    contact = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=contact, message=message_text)
    # Mark messages as read
    ChatMessage.objects.filter(sender=contact, receiver=request.user, is_read=False).update(is_read=True)
    messages_list = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=contact) | Q(sender=contact, receiver=request.user)
    )
    return render(request, 'chat/chat_detail.html', {
        'contact': contact,
        'messages_list': messages_list,
    })


@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if message:
            response = get_ai_response(message)
            return JsonResponse({'response': response, 'message': message})
    return render(request, 'chat/ai_chat.html')


@login_required
def send_message_view(request, user_id):
    contact = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=contact, message=message_text)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import ChatRoom, Message, Reply, Reaction
from django.db.models import Q
import random

# Consider chat.html is frontend of the chat func

@login_required
def group_chat_list(request):
    rooms = ChatRoom.objects.filter(members=request.user, is_group=True)
    return render(request, 'chat.html', {'rooms': rooms})

@login_required
def private_chat_list(request):
    chat = ChatRoom.objects.filter(members=request.user, is_group=False)
    return render(request, 'chat.html', {'chat': chat})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, members=request.user)
    messages = room.messages.order_by('-timestamp')

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "send_message":
            content = request.POST.get('content')
            file = request.FILES.get('file')

            if content or file:
                message = Message.objects.create(
                    chat_room=room,
                    sender=request.user,
                    content=content,
                    file=file
                )
                return JsonResponse({'status': 'success', 'message_id': message.id})
        
        elif action == "send_reply":
            message_id = request.POST.get('message_id')
            content = request.POST.get('content')
            file = request.FILES.get('file')
            parent_message = get_object_or_404(Message, id=message_id)
            
            reply = Reply.objects.create(
                message=parent_message,
                sender=request.user,
                content=content,
                file=file
            )
            return JsonResponse({'status': 'success', 'reply_id': reply.id})

        elif action == 'send_reaction':
            content_type = request.POST.get('content_type')
            object_id = request.POST.get('object_id')
            reaction = request.POST.get('reaction')

            ct = ContentType.objects.get(model=content_type)
            
            Reaction.objects.create(
                content_type=ct,
                object_id=object_id,
                user=request.user,
                reaction=reaction
            )
            return JsonResponse({'status': 'success'})

    return render(request, 'chat.html', {
        'room': room,
        'messages': messages,
    })

@login_required
def create_group_chat(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            room = ChatRoom.objects.create(name=name, is_group=True)
            room.members.add(request.user)
            return redirect('chat_room', room_id=room.id)
    return render(request, 'chat.html')

@login_required
def add_member(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.method == "POST":
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        room.members.add(user)
    return redirect('chat_room', room_id=room_id)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(Q(username__icontains=query))[:10]
    return JsonResponse({'users': [{'id': user.id, 'username': user.username} for user in users]})

@login_required
def create_private_chat(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            room = ChatRoom.objects.create(name=name, is_group=False)
            room.members.add(request.user)
            return redirect('chat_room', room_id=room.id)
    return render(request, 'chat.html')

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, members=request.user)
    messages = room.messages.order_by('-timestamp')[:50]
    data = []
    for message in messages:
        message_data = {
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'file': message.file.url if message.file else None,
            'reactions': [{'user': reaction.user.username, 'reaction': reaction.reaction} for reaction in message.reactions.all()],
            'replies': [],
        }
        for reply in message.reply_set.all():
            reply_data = {
                'id': reply.id,
                'sender': reply.sender.username,
                'content': reply.content,
                'timestamp': reply.timestamp.isoformat(),
                'file': reply.file.url if reply.file else None,
                'reactions': [{'user': reaction.user.username, 'reaction': reaction.reaction} for reaction in reply.reactions.all()],
            }
            message_data['replies'].append(reply_data)
        data.append(message_data)
    return JsonResponse({'messages': data})

def suggest(request):
    current_user = request.user

    all_group_chat = ChatRoom.objects.filter(is_group=True).exclude(member=current_user)
    suggested_group_chat=random.sample(list(all_group_chat), min(5, len(all_group_chat)))

    all_private_chat = ChatRoom.objects.filter(is_group=False).exclude(member=current_user)
    suggested_private_chat = random.sample(list(all_group_chat), min(5, len(all_group_chat)))

    group_chat_suggestions = [{'id': chat.id, 'name': chat.name} for chat in suggested_group_chat]
    private_chat_suggestions = [{'id': chat.id, 'name': chat.name} for chat in suggested_private_chat]
   
    return JsonResponse({
        'group_chats': group_chat_suggestions,
        'direct_chats': private_chat_suggestions
    })
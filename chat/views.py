from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PrivateChatRoom, GroupChatRoom, GroupMessage, PrivateMessage, Reply
from django.contrib.auth.models import User
from django.db.models import Q
import random


def PrivateChatList(request):
    private_chat_room = PrivateChatRoom.objects.filter(
        Q(member1=request.user) | Q(member2=request.user)
    )
    return render(request, 'private_chat_list_demo.html', {'private_chat_room': private_chat_room})

def GroupChatList(request):
    group_chat = GroupChatRoom.objects.filter(members=request.user)
    return render(request, 'group_chat_list_demo.html', {'group_chat': group_chat})

def SearchPrivateChat(request):
    query = request.GET.get('q', '')
    if query:
        search_result = PrivateChatRoom.objects.filter(
            Q(member1__username__icontains=query) | Q(member2__username__icontains=query),
            Q(member1=request.user) | Q(member2=request.user)
        )
    else:
        search_result = PrivateChatRoom.objects.filter(
            Q(member1=request.user) | Q(member2=request.user)
        )
    return render(request, 'private_chat_list_demo.html', {'private_chat_room': search_result, 'search_query': query})

def SearchGroupChat(request):
    query = request.GET.get('q', '')
    if query:
        search_result = GroupChatRoom.objects.filter(name__icontains=query, members=request.user)
    else:
        search_result = GroupChatRoom.objects.filter(members=request.user)
    return render(request, 'group_chat_list_demo.html', {'group_chat': search_result, 'search_query': query})


def create_group_chat(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        member_usernames = request.POST.get('members', '').split(',')
        members = [username.strip() for username in member_usernames]

        if group_name and member_usernames:
            members = User.objects.filter(username__in=member_usernames)
            if members.exists():
                group_chat = GroupChatRoom.objects.create(name=group_name)
                group_chat.members.add(*members)
                group_chat.members.add(request.user)
                return redirect('group_chat_list')
            else:
                error_message = "No users found with the given usernames."
        else:
            error_message = "Group name and members are required."
        return render(request, 'create_group_chat_demo.html', {'error': error_message})
    
    return render(request, 'create_group_chat_demo.html')

def create_private_chat(request):
    if request.method == 'POST':
        other_username = request.POST.get('username')
        try:
            other_user = User.objects.get(username=other_username)
            if other_user != request.user:
                chat_room, created = PrivateChatRoom.objects.get_or_create(
                    member1=request.user,
                    member2=other_user
                )
                if not created:
                    chat_room, created = PrivateChatRoom.objects.get_or_create(
                        member1=other_user,
                        member2=request.user
                    )
                return redirect('private_chat_list')
        except User.DoesNotExist:
            pass  # Handle user not found case if needed
    return render(request, 'create_private_chat_demo.html')

#Details of private chat
def show_private_messages(request, chat_id):
    chat_room = PrivateChatRoom.objects.get(id=chat_id)
    messages = PrivateMessage.objects.filter(private_chat_room=chat_room).order_by('timestamp')
    return render(request, 'private_chat_messages.html', {'chat_room': chat_room, 'messages': messages})

#details of group chats
def show_group_messages(request, chat_id):
    chat_room = GroupChatRoom.objects.get(id=chat_id)
    messages = GroupMessage.objects.filter(group_chat_room=chat_room).order_by('timestamp')
    replies = Reply.objects.filter(message__group_chat_room=chat_room).order_by('timestamp')
    return render(request, 'group_chat_messages.html', {'chat_room': chat_room, 'messages': messages, 'replies': replies})

def send_private_message(request, chat_id):
    if request.method == 'POST':
        chat_room = PrivateChatRoom.objects.get(id=chat_id)
        content = request.POST.get('content')
        img_file = request.FILES.get('img_file')
        PrivateMessage.objects.create(
            private_chat_room=chat_room,
            sender=request.user,
            content=content,
            img_file=img_file
        )
        return redirect('private_chat_messages', chat_id=chat_id)
    return redirect('private_chat_list')


def send_group_message(request, chat_id):
    if request.method == 'POST':
        chat_room = GroupChatRoom.objects.get(id=chat_id)
        content = request.POST.get('content')
        img_file = request.FILES.get('img_file')
        GroupMessage.objects.create(
            group_chat_room=chat_room,
            sender=request.user,
            content=content,
            img_file=img_file
        )
        return redirect('group_chat_messages', chat_id=chat_id)
    return redirect('group_chat_list')

def reply_group_message(request, chat_id, message_id):
    if request.method == 'POST':
        chat_room = GroupChatRoom.objects.get(id=chat_id)
        original_message = GroupMessage.objects.get(id=message_id)
        content = request.POST.get('content')
        img_file = request.FILES.get('img_file')
        Reply.objects.create(
            message=original_message,
            sender=request.user,
            content=content,
            img_file=img_file
        )
        return redirect('group_chat_messages', chat_id=chat_id)
    return redirect('group_chat_list')

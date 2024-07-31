from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PrivateChatRoom, GroupChatRoom, GroupMessage, PrivateMessage, Reply
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
import random

@login_required
def PrivateChatList(request):
    private_chat_room = PrivateChatRoom.objects.filter(
        Q(member1=request.user) | Q(member2=request.user)
    )
    return render(request, 'private_chat_list_demo.html', {'private_chat_room': private_chat_room})
@login_required
def GroupChatList(request):
    group_chat = GroupChatRoom.objects.filter(members=request.user)
    return render(request, 'group_chat_list_demo.html', {'group_chat': group_chat})
@login_required
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
@login_required
def SearchGroupChat(request):
    query = request.GET.get('q', '')
    if query:
        search_result = GroupChatRoom.objects.filter(name__icontains=query, members=request.user)
    else:
        search_result = GroupChatRoom.objects.filter(members=request.user)
    return render(request, 'group_chat_list_demo.html', {'group_chat': search_result, 'search_query': query})

@login_required
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
@login_required
def create_private_chat(request):
    if request.method == 'POST':
        other_username = request.POST.get('username')
        try:
            other_user = User.objects.get(username=other_username)
            if other_user != request.user:
                existing_chat=PrivateChatRoom.objects.filter(
                    Q(member1=request.user, member2=other_user) |
                    Q(member1 = other_user, member2 = request.user)
                ).first()

                if existing_chat:
                    messages.info(request, f"The chatroom already created")
                    return redirect('send_private_message', chat_id =existing_chat.id)
                else:
                    PrivateChatRoom.objects.create(member1=request.user, member2=other_user)
                    return redirect('private_chat_list')
        except User.DoesNotExist:
            pass
    return render(request, 'create_private_chat_demo.html')

@login_required
def show_private_messages(request, chat_id):
    chat_room = PrivateChatRoom.objects.get(id=chat_id)
    messages = PrivateMessage.objects.filter(private_chat_room=chat_room).order_by('timestamp')
    return render(request, 'private_chat_messages.html', {'chat_room': chat_room, 'messages': messages})

@login_required
def show_group_messages(request, chat_id):
    chat_room = GroupChatRoom.objects.get(id=chat_id)
    messages = GroupMessage.objects.filter(group_chat_room=chat_room).order_by('timestamp')
    replies = Reply.objects.filter(message__group_chat_room=chat_room).order_by('timestamp')
    members = chat_room.members.all().order_by('username')
    return render(request, 'group_chat_messages.html', {'chat_room': chat_room, 'messages': messages, 'replies': replies, 'members' :members})
@login_required
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

@login_required
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
@login_required
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

@login_required
def add_member_to_group_chat(request, chat_id):
    chat_room = GroupChatRoom.objects.get(id=chat_id)
    
    if request.method == 'POST':
        member_usernames = request.POST.get('members', '').split(',')
        members = [username.strip() for username in member_usernames]
        
        if members:
            users = User.objects.filter(username__in=members)
            if users.exists():
                added_members = []
                already_members = []
                not_found = []

                for user in users:
                    if user not in chat_room.members.all():
                        chat_room.members.add(user)
                        added_members.append(user.username)
                    else:
                        already_members.append(user.username)
                
                for member in members:
                    if not users.filter(username=member).exists():
                        not_found.append(member)

                if added_members:
                    messages.success(request, f"Added members: {', '.join(added_members)}.")
                if already_members:
                    messages.info(request, f"Already members: {', '.join(already_members)}.")
                if not_found:
                    messages.error(request, f"Usernames not found: {', '.join(not_found)}.")
            else:
                messages.error(request, "No valid usernames found.")
    
    return redirect('group_chat_messages', chat_id=chat_id)

@login_required
def exit_group_chat(request, chat_id):
    try:
        chat_room = GroupChatRoom.objects.get(id=chat_id)
        if request.user in chat_room.members.all():
            chat_room.members.remove(request.user)            
            if chat_room.members.count() == 0:
                chat_room.delete()
        else:
            messages.error(request, "You are not a member of this group chat.")
    except GroupChatRoom.DoesNotExist:
        pass
    
    return redirect('group_chat_list')

@login_required
def match_user(request):
    all_users = User.objects.exclude(id=request.user.id)
    
    existing_chats = PrivateChatRoom.objects.filter(
        Q(member1=request.user) | Q(member2=request.user)
    )
    chatted_with_users = User.objects.filter(
        Q(id__in=existing_chats.values('member1')) | Q(id__in=existing_chats.values('member2'))
    ).exclude(id=request.user.id)

    not_chatted_with_users = all_users.exclude(id__in=chatted_with_users)
    
    if not_chatted_with_users.exists():
        random_user = random.choice(not_chatted_with_users)
        existing_chat = PrivateChatRoom.objects.filter(
            Q(member1=request.user, member2=random_user) |
            Q(member1=random_user, member2=request.user)
        ).first()

        if existing_chat:
            messages.info(request, "You already have a chat with this user.")
            return redirect('send_private_message', chat_id=existing_chat.id)
        else:
            new_chat = PrivateChatRoom.objects.create(member1=request.user, member2=random_user)
            return redirect('private_chat_messages', chat_id=new_chat.id)
    else:
        messages.info(request, "No new users available for a random chat.")
    
    return redirect('private_chat_list')

@login_required
def match_group(request):
    all_users = User.objects.exclude(id=request.user.id)

    existing_groups = GroupChatRoom.objects.filter(members=request.user)

    chatted_with_users = User.objects.filter(
        Q(id__in=existing_groups.values('members'))
    ).exclude(id=request.user.id)

    not_chatted_with_users = all_users.exclude(id__in=chatted_with_users)

    # Group of 4 user, if not chatted members > 2 --> match
    group_size = 4
    required_members = group_size - 2

    if not_chatted_with_users.count() >= required_members:
        
        new_members = random.sample(list(not_chatted_with_users), required_members)
        
        group_name = "Random Group Chat" 
        group_chat = GroupChatRoom.objects.create(name=group_name)
        group_chat.members.add(request.user)
        group_chat.members.add(*new_members)
        
        return redirect('group_chat_messages', chat_id=group_chat.id)
    else:
        messages.info(request, "Not enough new users available to form a group.")
        return redirect('group_chat_list')

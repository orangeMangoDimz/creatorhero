from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import *
from .forms import ChatmessageCreateForm
from django.contrib import messages
from django.shortcuts import redirect


def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    # other_user = None
    # if chat_group.is_private:
    #     if request.user not in chat_group.members.all():
    #         raise Http404()
    #     for member in chat_group.members.all():
    #         if member != request.user:
    #             other_user = member
    #             break
            
    # if chat_group.groupchat_name:
    #     if request.user not in chat_group.members.all():
    #         print("curr_user: ", request.user)
            # if request.user.emailaddress_set.filter(verified=True).exists():
            #     chat_group.members.add(request.user)
            # else:
            #     messages.warning(request, 'You need to verify your email to join the chat!')
            #     return redirect('profile-settings')
    
    print("test")
    print("request methood: ", request.method)
    print("request.POST: ", request.POST)
    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            # context = {
            #     'message' : message,
            #     'user' : request.user or None
            # }
            # return render(request, 'partial/chat_message_p.html', context)

        
    context = {
        'chat_messages' : chat_messages, 
        'form' : form,
        # 'other_user' : other_user,
        'chatroom_name' : chatroom_name,
        'chat_group' : chat_group
    }
    
    return render(request, "chat.html", context)
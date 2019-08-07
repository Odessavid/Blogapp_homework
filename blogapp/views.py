from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Q


# Create your views here.

def index(request):
    user_list = User.objects.all()
    return render(request, 'blogapp/index.html', {'user_list': user_list})


def not_ready(request):
    return HttpResponse("Стрвница не готова")


def user_signin(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        profileform = ProfileForm(request.POST)
        # print(request.POST["username"])
        # print(request.POST["password"])
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(request.POST["password"])
            user.save()
            profileform.instance.user = user
            profileform.save()
            return redirect(reverse('index'))
    else:
        userform = UserForm()
        profileform = ProfileForm()
    return render(request, 'blogapp/signin.html', {'userform': userform, 'profileform': profileform})


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        data = request.POST
        # print(data['username'])
        # print(data['password'])

        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, 'blogapp/ERROR.html',
                              {'msg': 'The password is valid, but the account has been disabled!'})
        else:
            return render(request, 'blogapp/ERROR.html', {'msg': 'The username and password were incorrect.'})
    else:
        return render(request, 'blogapp/login.html')


def view_post(request, id):
    if request.method == 'POST':
        data = request.POST
        new_comment = Comment()
        new_comment.text = data['text']
        new_comment.user = request.user
        new_comment.post = Post.objects.get(id=id)
        new_comment.save()

    post = Post.objects.get(id=id)
    return render(request, 'blogapp/post.html', {'post': post})


def delete_com(request, id):
    comment = Comment.objects.get(id=id)
    post = comment.post
    comment.delete()
    return redirect(reverse('post', args=[post.id]))
        # render(request, 'blogapp/post.html', {'post': post})


# def create_post(request):
#     if request.method == 'POST':
#         postform = PostForm(request.POST)
#         if postform.is_valid():
#             postform.instance.user = request.user
#             postform.save()
#             my_id = postform.id
#             return redirect(reverse('post'+ my_id +'/'))
#     else:
#         postform = PostForm()
#     return render(request, 'blogapp/create_post.html', {'postform': postform})

def create_post(request):
    if request.method == 'POST':
        data = request.POST
        new_post = Post()
        new_post.title = data['title']
        new_post.text = data['text']
        new_post.user = request.user
        new_post.save()
        post_id = new_post.pk
        return redirect(reverse('post', args=[post_id]))

    else:
        return render(request, 'blogapp/create_post.html')


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        comment.text = data['text']
        comment.save()
        comment_id = comment.post.id
        return redirect(reverse('post', args=[comment_id]))
    else:
        return render(request, 'blogapp/edit_comment.html', {'comment': comment})


def password_changed(request):
    id = request.user.id
    # return HttpResponseRedirect(str(id)+ '/' )
    return render(request, 'blogapp/password_changed.html', {'id': id})


def profile(request, id):
    cur_user = User.objects.get(id=id)
    # cur_profile = cur_user.profile
    dic = {'cur_user': cur_user}
    return render(request, 'blogapp/profile.html', dic)


def edit_profile(request):
    if request.method == 'POST':
        profileform = ProfileForm(request.POST)
        if profileform.is_valid():
            cur_user = request.user
            cur_profile = cur_user.profile
            cur_user.email = request.POST['email']
            cur_profile.b_day = request.POST['b_day_year'] + '-' + request.POST['b_day_month'] + '-' + request.POST[
                'b_day_day']
            cur_profile.skype = request.POST['skype']
            cur_profile.facebook = request.POST['facebook']
            cur_profile.about = request.POST['about']



            cur_user.save()
            cur_profile.save()
            return redirect(reverse('profile', args=str(cur_user.id)))
    else:

        # profile = Profile.objects.get(user=request.user)
        profile = request.user.profile
        init = {
            'b_day': profile.b_day,
            'skype': profile.skype,
            'facebook': profile.facebook,
            'about': profile.about,
        }

        # user = UserForm(initial = {'email' : request.user.email})
        profileform = ProfileForm(initial=init)

    return render(request, 'blogapp/edit_profile.html', {'profileform': profileform})


def message(request,id):
    if request.method == 'POST':
        data = request.POST
        new_message = Message()
        new_message.text = data['text']
        new_message.sender = request.user
        new_message.receiver = User.objects.get(id=id)
        new_message.read = False
        new_message.save()
        return redirect(reverse('message', args=[id]))
    else:
        msg_snd = Message.objects.filter(sender__id=request.user.id).filter(receiver__id=id)
        msg_rcv = Message.objects.filter(receiver__id=request.user.id).filter(sender__id=id)
        msg = msg_rcv.union(msg_snd).order_by('date_time')
        for m in msg_rcv:
            if not(m.read):
                m.read = True
                m.save()

        usr = User.objects.all()


        # count = request.user.user_r.filter(read=False).count()

        u_list = []

        for u in usr:
            # condition = (Q(sender=request.user, receiver=u) | Q(sender=u, receiver=request.user))
            condition = Q(sender=u, receiver=request.user)

            count = Message.objects.filter(condition).filter(read=False).count()
            if count > 0:
                count = '({0})'.format(count)
            else:
                count = ''
            u_list.append( {'user':u ,'count': count})
        # s_msg = request.user.user_s.all()




        # s_list = set()
        # for u in r_usr:
        #     r_list.append(u.filter(read=False).count())
        #     s_list.add(m.sender)
        # sr_list = r_list.union(s_list)




        # for u in usr:
        #     u_list.append(u.user_r.filter(sender__id=request.user.id).filter(receiver__id=id).count())

        dic = {'msg': msg, 'usr': usr, 'id':id, 'u_list':u_list}
        return render(request, 'blogapp/message.html', dic)

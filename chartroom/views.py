from django.shortcuts import render, redirect, get_object_or_404 
from .models import Room, Topic, Message, User
from .forms import RoomForm, CreateUser, LoginUser, UserForm
from django.db.models import Q #this is to handle the search
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required


from django.db.models import Count
from django.shortcuts import render
from django.db.models import Q
from .models import Room, Topic, Message

 # Import get_object_or_404




def create_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUser()
    if request.method =="POST":
        form= CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')
    context ={'form':form}
    return render( request, 'chartroom/register.html', context)


def my_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginUser()
    if request.method =="POST":
       form = LoginUser(request, data=request.POST)
       if form.is_valid():
            username = request.POST.get('username')
            password =  request.POST.get('password')
            user = authenticate(username=username ,  password=password)
            if user is not None:
               auth.login(request, user)
               return redirect("home")
    context = {'form1': form}


    return render(request, 'chartroom/my-login.html',context)




def home(request):
    q = request.GET.get('q', '')  # Default to an empty string if 'q' is not provided
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )  # Use OR (|) to match any field
    
    # Total room count
    room_count = rooms.count()

    # Fetch topics and annotate with the count of related rooms
    topics = Topic.objects.annotate(room_count=Count('room'))  

    # Get messages related to the searched topics
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {
        'room_count': room_count,
        'rooms': rooms,
        'topics': topics,  # Now topics include room_count
        'room_messages': room_messages,
    }

    return render(request, 'chartroom/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    print("Participants:", participants) 

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'chartroom/room.html', context)


# create Room
@login_required(login_url='my-login')
def creatRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":

        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name= topic_name)

        Room.objects.create(
            host= request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        return redirect('home')
    context = {'form':form,
               'topics':topics
               }
    return render(request, 'chartroom/create-room.html', context)

@login_required(login_url='my-login')




@login_required(login_url='my-login')

def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)  # Correct: Use get_object_or_404 to get a single room
    form = RoomForm(instance=room)
    topics = Topic.objects.all()  # Correct: Use all() to get all topics

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this.')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save() # important to save the room.
        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
        'room': room,
    }
    return render(request, 'chartroom/update-room.html', context)


# delete
@login_required(login_url='my-login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse(' yor are not allow to delete this ')
    if request.method == "POST":
        room.delete()

        return redirect('home')
    return render(request, 'chartroom/delete.html', {'obj': room, 'request': request})


# logout
@login_required(login_url='my-login')
def my_logout(request):
    auth.logout(request)
    # messages.success(request, "Logout Success")
    return redirect("my-login")


@login_required(login_url='my-login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    # Check if the current user is the owner of the message
    if request.user != message.user:  # message.user should point to the user who created the message
        return HttpResponse('You are not allowed to delete this.')

    # If the request method is POST, delete the message
    if request.method == "POST":
        message.delete()
        return redirect('home')  # Redirect to the home page after deletion

    # If the request method is GET, render the confirmation page
    return render(request, 'chartroom/delete.html', {'obj': message})

@login_required(login_url='my-login')
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    print(f"Profile User ID: {user.id}")

    room_messages = Message.objects.filter(user=user).order_by('-created')[:10]

    for message in room_messages:
        print(f"Message User ID: {message.user.id}")

    topics = Topic.objects.annotate(room_count=Count('room'))

    room_count = Room.objects.count()

    # Add this line to define rooms
    rooms = Room.objects.filter(host=user)

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'chartroom/profile.html', context)

@login_required(login_url='my-login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'chartroom/update-user.html', {'form':form})
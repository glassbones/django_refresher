from django.shortcuts import render, redirect
from apps.profiles.models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile) # <-- args here fill the form
    userHasUpdated = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            userHasUpdated = True

    context = {
        'profile': profile,
        'form': form,
        'userHasUpdated': userHasUpdated
    }

    return render(request, 'profiles/myprofile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    query_set = Relationship.objects.invitations_received(profile)

    context = {'query_set': query_set}
    return render(request,'profiles/my_invites.html', context)

def invite_profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_available_relationships(user)

    context = {'query_set': query_set}
    return render(request,'profiles/to_invite_profile_list.html', context)

# same as ProfileListView just a function instead of a class
# (start) this code is not being used
def profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles(user)
    context = {'query_set': query_set}
    return render(request,'profiles/profile_list.html', context)
# (end) this code is not being used

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    #overiding attr name
    context_object_name = 'query_set'

    #overiding default method
    def get_queryset(self):
        query_set = Profile.objects.get_all_profiles(self.request.user)
        return query_set

    #overiding default method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get( username__iexact=self.request.user ) # "username__iexact" helps prevent errors?
        profile = Profile.objects.get(user=user)
        context['profile'] = profile

        # grabing all relationships involving the user
        relations_received = Relationship.objects.filter(sender=profile)
        relations_sent = Relationship.objects.filter(receiver=profile)

        # turning those lists of relationships into lists of users
        received_rel_users = []
        sent_rel_users = []

        for rel in relations_received:
            received_rel_users.append(rel.receiver.user)

        for rel in relations_sent:
            sent_rel_users.append(rel.sender.user)

        context['received_rel_users'] = received_rel_users
        context['sent_rel_users'] = sent_rel_users
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context
    
def send_invitation(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk') # target
        user = request.user # origin
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
    
def remove_friend(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk') # target
        user = request.user # origin
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        # Unfortunately we dont know which user originally created the relationship (sent the friend request)
        # we have to query the sent relationships of the user and the pk here

        rel = Relationship.objects.get(
            # user sent the relationship invite
            (Q(sender=sender) & Q(receiver=receiver)) | 
            # user received the relationship invite
            (Q(sender=receiver) & Q(receiver=sender)) 
        )

        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

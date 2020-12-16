from django.shortcuts import render
from apps.profiles.models import Profile, Relationship
from .forms import ProfileModelForm
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

def profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_all_profiles(user)

    context = {'query_set': query_set}
    return render(request,'profiles/profile_list.html', context)

def invite_profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.get_available_relationships(user)

    context = {'query_set': query_set}
    return render(request,'profiles/to_invite_profile_list.html', context)
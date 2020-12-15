from django.shortcuts import render
from apps.profiles.models import Profile
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


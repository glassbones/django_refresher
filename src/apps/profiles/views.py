from django.shortcuts import render
from apps.profiles.models import Profile

# Create your views here.
def my_profile_view(request):
    for var in vars(Profile):
        print(var)
    obj = Profile.objects.get(user=request.user)
    #context = {}

    return render(request, 'profiles/myprofile.html', {'obj': obj})


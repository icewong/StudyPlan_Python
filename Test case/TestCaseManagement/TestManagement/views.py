from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/testcase/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'testcase/Login.html', {})

def user_login_newpwd(request):
    return render(request,'testcase/Login.html',{'PromptInfo':'Please login with new password.'})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_setting(request):
    modified = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        curUser = User.objects.get(username=request.user.username)
        if curUser.check_password(oldpwd):
            curUser.set_password(newpwd)
            curUser.save()
            return HttpResponse('<p>You were changed password successfully.</p><a href="/loginWithNewPwd/">Login Again</a>')
        else:
            response = HttpResponse("Your old password is wrong, please input the correct password.")
            response.status_code=400
            return response
    else:
        return render(request,'testcase/UserSettings.html',context={})
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.utils.http import is_safe_url


from accounts.forms import LoginForm, RegisterForm

#from .forms import ParentSignUpForm, SchoolSignUpForm, VendorSignUpForm
from .models import User



class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)

        return super(LoginView, self).form_invalid(form)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_parent:
            return redirect('parent:parent_home')
        elif request.user.is_school:
            return redirect('school:school_home')
        elif request.user.is_vendor:
            return redirect('vendor:vendor_home')
    return render(request, '/home.html')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'

#class ProfileView(CreateView):
 #   template_name = 'accounts/profile.html'

def profile_view(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {"user":user})
    




from django.views.generic import CreateView
from .forms import RegistrationForm


# Create your views here.
class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = '/'
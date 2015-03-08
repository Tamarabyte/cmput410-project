from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages

from Hindlebook.forms.auth_forms import RegistrationForm

class RegistrationView(FormView):
    
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('register')

    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.save();
        messages.add_message(self.request, messages.SUCCESS,
            'You have successfully registered. An admin should confirm your account shortly.')
        return super(RegistrationView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('login')
    


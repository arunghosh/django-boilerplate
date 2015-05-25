from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, RedirectView, FormView
# from django.views.generic.edit import FormView

from django.contrib import messages


class AbstractFormView(FormView):
    title = None
    success_message = "Successfully Updated"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.save():
            messages.success(self.request, self.success_message)
        else:
            return self.form_invalid(form)
        return super(AbstractFormView, self).form_valid(form)


def handle_success(request, message, url=None):
    ''' Redirect to home if no success url provied
    '''
    if not url:
        url = reverse('home')
    messages.success(request, message)
    return redirect(url)


from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, RedirectView
from django.views.generic.list import ListView
# from django.views.generic.edit import FormView

from django.contrib import messages


class FormView(View):
    title = None
    success_message = "Updated"
    success_url = reverse_lazy('home')

    def get(self, request, initial=None):
        if initial:
            form = self.form(initial=initial)
        else:
            form = self.form()
        return self._render(request, form)

    def post(self, request, instance=None):
        form = self._get_form(request, instance)
        if form.save():
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        return self._render(request, form)

    def _get_form(self, request, instance):
        if instance:
            form = self.form(request.POST, request.FILES, instance=instance)
        else:
            form = self.form(request.POST)
        return form

    def _render(self, request, form):
        return render(request, self.template, {
          'form': form, 
          'title': self.title,
          })


def handle_success(request, message, url=None):
    ''' Redirect to home if no success url provied
    '''
    if not url:
        url = reverse('home')
    messages.success(request, message)
    return redirect(url)


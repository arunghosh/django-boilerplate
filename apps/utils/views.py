from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages


class FormView(View):
    success = "Updated"
    submit_name = "Save"
    popup = False
    title = None
    success_url = reverse_lazy('home')

    def get(self, request, initial=None):
        if initial:
            form = self.form(initial=initial)
        else:
            form = self.form()
        return self._render(request, form)

    def post(self, request, instance=None):
        if instance:
            form = self.form(request.POST, request.FILES, instance=instance)
        else:
            form = self.form(request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, self.success)
                return redirect(self.success_url)
        return self._render(request, form)

    def _render(self, request, form):
        return render(request, self.template, {
          'form': form, 
          'submit_name' : self.submit_name, 
          'popup': self.popup,
          'title': self.title,
          })


def handle_success(request, message, url=None):
    if not url:
        url = reverse('home')
    messages.success(request, message)
    return redirect(url)


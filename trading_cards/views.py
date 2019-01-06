from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
import subprocess
import os
import base64

from .forms import *


class DefaultFormsetView(FormView):
    template_name = "cardform.html"
    form_class = CardForm
    success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()

        if form.is_valid():
            output = self.form_valid(form)
            return redirect("http://"+request.get_host() + output)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Create new directory to store output
        directory = tempfile.mkdtemp(prefix=base64.urlsafe_b64encode(os.urandom(64)).decode().replace('=', ''),
                                     dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output'))
        d = form.cleaned_data
        p = subprocess.Popen(["pdflatex",
                              "-output-directory", directory,
                              "-synctex=1", "-interaction=nonstopmode",
                              "\\def\\copyrightname{{{}}}"
                              "\\def\\overlay{{{}}}"
                              "\\def\\backgroundimage{{{}}}"
                              "\\def\\playername{{{}}}"
                              "\\def\\playernumber{{{}}}"
                              "\\def\\position{{{}}}"
                              "\\def\\motto{{{}}}"
                              "\\def\\function{{{}}}"
                              "\\input{{document}}".format(
                                  d['copy'],
                                  d['team'],
                                  d['image'].name,
                                  d['name'],
                                  d['number'],
                                  ', '.join(d['position']),
                                  d['phrase'],
                                  d['func'])],
                             cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'latex'))
        p.wait()
        # Redirect to file

        return directory[len(os.path.dirname(os.path.realpath(__file__))):] + "/document.pdf"

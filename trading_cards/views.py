from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
import subprocess
import os
import base64
from django.utils.text import slugify
from django.http import HttpResponse
import shutil

from .forms import *


def latexCleanText(text):
    new = ""
    for c in text:
        c = {
            '#': r'\#',
            '$': r'\$',
            '%': r'\%',
            '^': r'\^{}',
            '&': r'\&',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\~{}',
            '\\': r'\textbackslash{}',
        }.get(c, c)
        new += c
    return new


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
            return output
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Create new directory to store output
        directory = tempfile.mkdtemp(prefix=base64.urlsafe_b64encode(os.urandom(64)).decode().replace('=', ''),
                                     dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output'))
        d = form.cleaned_data
        p = subprocess.Popen(["xelatex",
                              "-output-directory", directory,
                              "-synctex=1", "-interaction=nonstopmode",
                              (r'\def\copyrightname{{{}}}\def\overlay{{{}}}\def\backgroundimage{{{}}}' +
                              r'\def\playername{{{}}}\def\playernumber{{{}}}\def\position{{{}}}' +
                              r'\def\motto{{{}}}\def\function{{{}}}\input{{document}}').format(
                                  latexCleanText(d['copy']),
                                  d['team'],
                                  d['image'].name,
                                  latexCleanText(d['name']),
                                  latexCleanText(d['number']),
                                  latexCleanText(', '.join(d['position'])),
                                  latexCleanText(d['phrase']),
                                  d['func'])],
                             cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'latex'))
        p.wait()
        file_path = directory + "/document.pdf"
        fsock = open(file_path, "rb")
        response = HttpResponse(fsock, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+slugify(d['name'])+'_'+slugify(d['team'])+'.pdf"'
        fsock.close()
        shutil.rmtree(directory)

        return response


class PrivacyView(TemplateView):
    template_name = "privacy.html"

class ImpressumView(TemplateView):
    template_name = "impressum.html"
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
from django.conf import settings
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
            '\n': r'\\',
            '\r': '',
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
        xelatexCommand = ["xelatex",
                              "-output-directory", directory,
                              "-synctex=1", "-interaction=nonstopmode",
                              (r'\def\copyrightname{{{}}}\def\overlay{{{}}}\def\teamname{{{}}}\def\backgroundimage{{{}}}' +
                              r'\def\playername{{{}}}\def\playernumber{{{}}}\def\position{{{}}}' +
                              r'\def\motto{{{}}}' +
                              r'\def\cata{{{}}}\def\catb{{{}}}\def\catc{{{}}}\def\catd{{{}}}' +
                              r'\def\vpositioncolor{{{}}}' +
                              r'\def\vnamecolor{{{}}}' +
                              r'\input{{document}}').format(
                                  latexCleanText(d['copy']),
                                  d['team'],  # Overlay
                                  settings.TEAMNAMES[d['team']],  # actual name
                                  d['image'].name,
                                  latexCleanText(d['name']),
                                  latexCleanText(d['number']),
                                  latexCleanText('/'.join(d['position'])),
                                  latexCleanText(d['phrase']),
                                  d['cata'], d['catb'], d['catc'], d['catd'],
                                  settings.COLOR_POSITION[d['team']],
                                  settings.COLOR_NAME[d['team']])]
        p = subprocess.Popen(xelatexCommand,
                             cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'latex'))
        p.wait()
        p = subprocess.Popen(xelatexCommand, # Run two times, because latex is latex
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

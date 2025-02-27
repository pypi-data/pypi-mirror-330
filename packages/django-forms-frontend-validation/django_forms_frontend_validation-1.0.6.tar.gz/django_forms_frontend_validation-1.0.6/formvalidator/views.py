from django.shortcuts import render

from .forms import SampleForm

from .form_utils import FormsValidator


# Create your views here.
def sample(request):
    """
    Sample form view for demonstration purposes only.
    Will provide an example of using the forms.bundle.js file as an imported module.
    Will also not use the settings.py variables.
    """
    title = "Form Validator Sample"
    template = "formvalidator/sample.html"

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SampleForm()

    context = {
        "form": form,
        "title": title,
    }
    return render(request, template, context)


def sample2(request):
    """
    Another sample form view for demonstration purposes only.
    This demo will show how to use the forms.bundle.js file as a CDN, and using the settings variables
    for the configuration.
    """
    title = "Form Validator Sample 2"
    template = "formvalidator/sample2.html"
    form_validator = FormsValidator()

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SampleForm()

    context = {
        "form": form,
        "title": title,
        "form_validator": form_validator.get_context(),
    }
    return render(request, template, context)

# django-forms-frontend-validation App
___

This project provides a comprehensive system for handling and validating HTML forms in Django applications. It combines client-side JavaScript-based validation and server-side Python logic for robust form processing.

The application is designed to streamline the process of form validation, ensuring user inputs meet the requirements before submitting them to the server. The system offers features like automatic required-field validation, error handling, and dynamic CSRF token management for secure data transmission.

## Features
- Client-Side Validation: 
  - Automatically validates required fields.
  - Displays validation errors inline and dynamically updates them upon correction.
  - Adds asterisks to labels of required fields for better user clarity.
- Server-Side Settings:
  - Control which forms and fields to ignore during validation.
  - Define validation behavior, such as enforcing checks only on form submission.
- Integration with Django Settings:
  - Use Django's settings to dynamically configure validation rules.
- Secure Fetch Calls:
  - Includes CSRF token management for secure AJAX-based form submissions.

## Usage
### Installation
1. Install the Django project
    ```bash
   pip install django-frontend-forms-validation
   ```
### Setting Up
1. Define Settings in settings.py
   - Add `formvalidator` to installed apps.
      ```python
      INSTALLED_APPS = [
        ...,
        'formvalidator',
      ]
      ```
   - Configure the following variables to customize the behavior, after importing the form settings.
      ```python
     from formvalidator.settings import * 
     
     IGNORED_CLASSES = ['example-class', 'example-class-2', ...] #  replace these classes with your own
      IGNORE_VALIDATION = ['example-ignore-validation', ...]  # replace these classes with your own
      VALIDATE_ONLY_ON_SUBMIT = ['all']  # Options: "__all__", specific class names, or leave empty.
     # validate only on submit will only validate the inputs when the submit button is clicked
     # leaving it the list blank will allow for validation to happen on focus-out/onblur of an input
      ```
2. Initial Forms:
   - Ensure the `_InitializeForms` method is called during page load to attach validation logic to forms dynamically.
   To your HTML template with the form, add this.
   ```html
   <script src="{% static 'formsvalidator/js/forms.bundle.js' %}"></script> 
   <script>
    // fv (formsvalidator) is exported from forms.bundle.js
    window.addEventListener("load", () => {
        let ignoredClasses = {{ form_validator.ignored_classes|safe }}; // add more classes that represent forms you want this script to ignore.
        let ignoreValidation = {{ form_validator.ignore_validation|safe }}; // add any form classes that you want to ignore validation
        let validateOnlyOnSubmit = {{ form_validator.validate_only_on_submit|safe }}; // for hitting all forms make index 0 either __all__, all, * or leave blank for false or use false
        let forms = document.getElementsByTagName("form");
        // if (form || userForm) {
        if (forms.length > 0) {
            // calling specific functions on all forms
            fv._InitializeForms(forms, ignoredClasses, ignoreValidation, validateOnlyOnSubmit);
        }
    });
   </script>
   ```
   **Quick Note* - if your template is not finding `'formvalidator/js/forms.bundle.js'`, make sure either `STATICFILES_DIRS` is defined within your settings.py files, or if on production `STATIC_ROOT` is defined. If `STATIC_ROOT` is defined then make sure to run:
    ```bash
   ./manage.py collectstatic
   ```

3. Server-Side Context:
   - Use the `FormsValidator` class to pass configuration to templates:
   ```python
    from formvalidator.form_utils import FormsValidator
   
   
    def my_view(request):
        form_validator = FormsValidator()
        context = {
            'form_validator': form_validator.get_context(),
        }    
        return render(request, 'my_template.html', context)
   ```
4. Add `div` Groups to the HTML Form:
   - The JavaScript in this project relies on each form field being wrapped inside an outer div with the classname of ```form-group```.
   - It helps set apart each input from other inputs within the form.
   - Here is an example of the setup:
   ```html
    <form ...>
        {% csrf_token %}
   
        <div class="form-group">
            <label for="field1">Field 1</label>
            <input type="text" name="field1">
        </div>
   
        <div class="form-group">
            <label for="field2">Field 1</label>
            <input type="text" name="field2">
        </div>
        
        <-- Adding the rest of the form groups below -->
        ...
    </form>
    ```
   - If iterating through each form input using the ```form``` context variable:
    ```html
    <form ...>
        {% csrf_token %}
        
        <-- iterating through each form field -->
        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.name }}">{{ field.label }}</label>
                {{ field }}
            </div>
        {% endfor %}
    </form>
    ```
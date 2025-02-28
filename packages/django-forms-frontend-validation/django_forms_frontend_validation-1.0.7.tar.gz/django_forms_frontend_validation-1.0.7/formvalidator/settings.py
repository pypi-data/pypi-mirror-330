# ##### Form Configs #####
# A list of HTML classes of forms you want to ignore, completely
IGNORED_CLASSES = []

# Ignoring validation doesn't automatically assume you're omitting the form from being
# the form submittal process. It literally just means you would like to ignore all validation.
IGNORE_VALIDATION = [] + IGNORED_CLASSES

# A list of classes where the validation is done only after the submit button has been clicked.
# the types can be boolean, string, or list
# the string keyword options are 'all', '__all__', '*'
# if you would like to keep the type as an array, but still want to hit all forms, you can just set
# index 0 as one of those keywords
VALIDATE_ONLY_ON_SUBMIT = []
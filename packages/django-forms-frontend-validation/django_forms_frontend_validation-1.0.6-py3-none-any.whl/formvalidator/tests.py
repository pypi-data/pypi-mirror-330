from django.test import TestCase

from .form_utils.form_utils import FormsValidator


# Create your tests here.
class GetContextTest(TestCase):
    def setUp(self):
        self.form_validator = FormsValidator()
        self.context = self.form_validator.get_context()

    def test_get_context(self):
        """Ensuring that the context variable is set correctly"""
        self.assertEqual(type(self.context), dict, msg="The context variable is not a dictionary datatype")

    def test_context_variables(self):
        """Tests that the context variables are set correctly"""
        context_keys = self.context.keys()
        correct_keys = ["ignored_classes", "ignore_validation", "validate_only_on_submit"]
        for key in context_keys:
            self.assertTrue(key in correct_keys, msg=f"The context variable {key} is missing")

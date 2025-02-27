from setuptools import setup, find_packages

setup(
    name='django-forms-frontend-validation',
    version='1.0.6',
    packages=find_packages(exclude=['core*']),
    include_package_data=True,
    license='MIT',  # Use the license that applies to your project
    description='A Django app for front-end form validation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrew Kyle',
    author_email='andrew.kyle92@yahoo.com',
    url='https://github.com/andrew-kyle92/django-forms-frontend-validation',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'Django>=3.2',  # Specify the Django version you want to support
    ],
)

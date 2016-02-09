from distutils.core import setup

setup(
        name='django-data-versioning',
        version='0.1',
        packages=['data_versioning'],
        url='http://barlwks0010:7990/projects/ASPX/repos/django-data-versioning/',
        license='',
        author='Nacho Gentile',
        author_email='nacho.gentile@gameloft.com',
        description='Allows to create different versions of data in different databases in run-time. Versions can be associated to a user and browse in the admin interface.',
        install_requires=[
            'django'
        ]
)

django-starterkit-userauth
==========================

All I want is logged in users.

I want public facing login forms.

I want logged in (stateful) users to be able to access/see more stuff.

---

Therefore I need:
- login form "block"
- password retreival
- password change


Some example templates:
- forms
- content with `{% permission %}` tags

The intention is to be marginally more opinionated than native Django.

---

I want to do this in a way that is using Django utilities and the Django "recommended" way as much as possible (https://docs.djangoproject.com/en/dev/topics/auth/).

As simple as possible and rejecting additional features _except_ for the following 2:
- using `email` as Login
- overriding built-in `max_length`


For fully featured registration and authentication see:

- [https://www.djangopackages.com/grids/g/profiles/](https://www.djangopackages.com/grids/g/profiles/)
- [https://www.djangopackages.com/grids/g/authentication/](https://www.djangopackages.com/grids/g/authentication/)
- [https://www.djangopackages.com/grids/g/registration/](https://www.djangopackages.com/grids/g/registration/)
- [https://www.djangopackages.com/packages/p/django-user-accounts/](https://www.djangopackages.com/packages/p/django-user-accounts/)

---

### Installation Instructions

Copy "accounts" directory in to your project.

Optionally copy over the templates from the "templates" directory as meet your needs.

Add to your INSTALLED_APPS:
    INSTALLED_APPS = [
        ...
        'accounts',
        ...
    ]


Add the following to your 'settings.py':

    AUTH_USER_MODEL = 'accounts.Profile'
    LOGIN_URL = 'accounts:login'
    LOGOUT_URL = 'accounts:logout'
    #LOGIN_REDIRECT_URL = '/' ## Can add if you want.



### The Process

Despite the simplicity of the some opinionation was necessary.

Firstly there is a major decision in to whether to *extent* or *inherit* from the built-in `django.contrib.auth.User` mode.

For an explanation about this watch this talk:

[http://www.youtube.com/watch?v=KHg6AoExYjs](http://www.youtube.com/watch?v=KHg6AoExYjs)


If you want just add some more basic attributes, you can:

    class Employee(models.Model):
        user = models.OneToOneField(User)
        department = models.CharField(max_length=100)


If you want to change some of the important nuts-and-bolts built-in attributes, you can::

    class MyUser(AbstractBaseUser):
        my_username =  models.CharField(max_length=40, unique=True,
                                        db_index=True)
        ...
        USERNAME_FIELD = 'my_username'


[https://docs.djangoproject.com/en/1.6/topics/auth/customizing/#extending-the-existing-user-model](https://docs.djangoproject.com/en/1.6/topics/auth/customizing/#extending-the-existing-user-model)

We are using the more serious form to meet our only 2 feature requirements (which are: using email as login, overriding max_length)


#### Application

We are making a new application to put the additional forms, tests and views in.

This is named `accounts` and `Profile` in homage to the deprecated django docs.
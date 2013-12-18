django-starterkit-userauth
==========================

### All I want is logged in users!

Public users that is, with public facing login forms. I want logged in (stateful) users to be able to have better access than stateless visitors.

#### Therefore I need:

 - login form/logout
 - password retreival
 - password change
 - `{% if user.is_authenticated %} ...` tags wherever I want in my templates

The intention is to be marginally more opinionated than native Django.

This project is designed to be a starting point ([cookiecutter](https://github.com/pydanny/cookiecutter-django)-style) whence you can make your own customisations.

---

I want to do this in a way that is using Django utilities and the Django "recommended" way as much as possible (https://docs.djangoproject.com/en/dev/topics/auth/).

Nothing fancy! Only modifying the following 2 attributes:

- using `email` as Login
- overriding built-in `max_length`


For fully featured (many bells-and-whistles) registration and authentication see:

- [https://www.djangopackages.com/grids/g/profiles/](https://www.djangopackages.com/grids/g/profiles/)
- [https://www.djangopackages.com/grids/g/authentication/](https://www.djangopackages.com/grids/g/authentication/)
- [https://www.djangopackages.com/grids/g/registration/](https://www.djangopackages.com/grids/g/registration/)
- [https://www.djangopackages.com/packages/p/django-user-accounts/](https://www.djangopackages.com/packages/p/django-user-accounts/)

---

### Installation Instructions

Copy `\accounts` directory in to your project.

Optionally copy over the templates that you want from the `\templates\accounts` directory.

Add to your `INSTALLED_APPS`:

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


Add `url(.., include('accounts.urls'))` to `urls.py`, eg:

    urlpatterns = patterns('',
        ...
        ## Custom user models
        url(r'^profile/', include('accounts.urls')),
        ...
    )



Modify `/accounts/models.py` to meet your needs. There is a bunch of handy stuff there but you can modify/delete however you'd like, eg:

    class Profile(..):
        ...
        email = models.EmailField('email address', max_length=254, unique=True)
        """ Email to be used as username. """
        ...
        USERNAME_FIELD = 'email'
        ...


#### IMPORTANT! Note about Migrations

IMPORTANT: Custom user model + Migrations *do not play well together*

The script below *modifies your migrations* in order for them to work with custom user models:

[https://github.com/elena/scripts.elena.github.io/blob/master/_posts/django/migrate_auth-replace/script.py](https://github.com/elena/scripts.elena.github.io/blob/master/_posts/django/migrate_auth-replace/script.py)

This is an imperfect solution (as frozen versions of the migrations are modified to being more general therefore less accurate).

Django migrations are changing rapidly in the next version so hopefully this will be repaired and this script will no longer be necessary.


---

### The Process

Despite the simplicity of the some opinionation was necessary.

Firstly there is a major decision in to whether to *extent* or *inherit* from the built-in `django.contrib.auth.User` mode.

For an explanation about this watch this talk:

[http://www.youtube.com/watch?v=KHg6AoExYjs](http://www.youtube.com/watch?v=KHg6AoExYjs)


#### Option A (simpler: just adding to existing):

If you want just add some more basic attributes, you can:

    class Employee(models.Model):
        user = models.OneToOneField(User)
        department = models.CharField(max_length=100)


#### Option B (more serious: modify existing):

If you want to change some of the important nuts-and-bolts built-in attributes, you can:

    class MyUser(AbstractBaseUser):
        my_username =  models.CharField(max_length=40, unique=True,
                                        db_index=True)
        ...
        USERNAME_FIELD = 'my_username'


[https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model](https://docs.djangoproject.com/en/1.6/topics/auth/customizing/#extending-the-existing-user-model)


Or alternatively (as is a common use case):

    class MyUser(AbstractBaseUser):
        email =  models.EmailField(unique=True, db_index=True)
        ...
        USERNAME_FIELD = 'email'


[https://docs.djangoproject.com/en/dev/ref/models/fields/#emailfield](https://docs.djangoproject.com/en/dev/ref/models/fields/#emailfield)


This project uses the more serious form to meet our only 2 feature requirements (which are: using email as login, overriding max_length)


---

This is named `accounts` and `Profile` in homage to the deprecated django docs.
# Django Gumroad Clone

### link to the deployed app website: https://djgumroad-app-xmuhn.ondigitalocean.app/

Build a clone of gumroad.com. Gumroad is a place where creators can sell their digital products and get paid. I have used the Stripe Payments and Stripe Connect to handle accept payments and sending payouts to all the creators.

## Features
- Full featured "E-Commerce app" where creators can sell their digital products and get paid. 
- Sending Email (with SendInBlue API )
- Simulate a real payment process by using the Stipe API. Use Stripe Payments and Stripe Connect to handle accept payments and sending payouts to all the creators.
- Create,  View , Update and delete Products (all Class-Based-View)
- Secured app by applying security principles:
        - **CSRF token**
        - Only using **Https**
        - Use the LoginRequiredMixin to secure each view
        - Authorization and Authentication the users using the **allauth library**
        - Secure the Frontend with Django template engine ({% request.is.authenticated %})
        - Secure the sensetive info by using the **environ library** to store all **enviroment veriabels**
- **Signals** event dispatchers like – pre_save, post_save
- Uploading files options (Images and Documents)
- Combining the **“Flash message”** feature
- Designed web app displays for users
- Customized admin site Interface
- Using the **Cookiecutter package**, a project template for advacned production-ready Django projects.



## Running the project
TODO




License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy djgumroad

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

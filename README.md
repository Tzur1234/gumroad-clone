# Django Gumroad Clone

### link to the deployed app website: https://djgumroad-app-xmuhn.ondigitalocean.app/
### link to demo video: https://youtu.be/-RqRnl6G4UE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This time I have built a clone of gumroad.com. Gumroad is a place where creators can sell their digital products and get paid. I have used the Stripe Payments and Stripe Connect to handle accept payments and sending payouts to all the creators.

This project shows demonstrate the work with Different API's and leverage the usage of them   

## Features
- Full featured "E-Commerce app" where creators can sell their digital products and get paid. 
- Sending emails with SendInBlue API
- Simulate a real payment process by using the Stripe API. Use Stripe Payments and Stripe Connect to handle accept payments and sending payouts to all the creators.
- Create,  View , Update and delete Products (all Class-Based-View)
- Secured app by applying security principles:
     - **CSRF token**
     - Only using **Https**
     - Use the **LoginRequiredMixin** allow only authenticated users to access some views
     - **Authorization and Authentication** the users using the **allauth library**
     - Secure the Frontend with Django template engine ({% **request.is.authenticated** %})
     - Secure the sensetive info by using the **environ library** to store all **enviroment veriabels**
- **Signals** event dispatchers like – pre_save, post_save
- Uploading files options (Images and Documents)
- Combining the **“Flash message”** feature
- Designed web app displays for users
- Customized admin site Interface
- Using the **Cookiecutter package**, a project template for advacned production-ready Django projects.




## Running the project
1. Create your own virtual environment , and  don't forget to activate it | [toturial link](https://bit.ly/3YQlTDn)
2. Install all of the packages which is mentioned in ```requirements/local.txt``` file
3. Create a new file named ```.env``` inside the root of you project folder
4. Copy all of the variables inside ```.env.template``` to your ```.env``` file and fill your own values inside 
5. Download **Postgresql** and configure the connection parameters with to your own db in ```settings.py```, [see link for tutorial for more explanation](http://shorturl.at/dxEZ6) 
6. Learn how to create your own ```SECRET_KEY``` : https://bit.ly/42atuj1 and copy it to ```.env``` file.
You can find all the [settings you have to config here](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).
7. Create an account in Stripe
8. Copy and fill the DJANGO_SECRET_KEY and STRIPE_PUBLIC_KEY from your account 
9. Create a secure https host using ngrock (https://dashboard.ngrok.com/get-started/your-authtoken) and add the new secure host to your ALLOWED_HOST in config/settings/local.py
10. Create new Webhooks in Stripe and connect to ```https://<your ngrock secured host>/webhooks/stripe/```
11. Create a superuser for your app (it will be used as the first user) run in the terminal ```python manage.py createsuperuser ```
12. Run ```export READ_DOT_ENV_FILE=True``` inside your terminal so that your environment variables file will be read.
13. Run ```python manage.py makemigrations``` inside your terminal
14. Run ```python manage.py migrate``` inside your terminal
15.  After migrating, Run ```python manage.py runserver``` inside your terminal to run the server

If you have closely followed the instructions, you suppose the see the home html page and you can loging thesystem using the superuser credentials



## Get strated as a User

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

### Buy A Product
1. Go to discovery page
2. select the desired product you want to purchase
3. Click on the top green button "Chaeckout"
4. In the paying page fill a dunky card details:
      - card number must be: 4242 4242 4242 4242 the other details doesn't matter
6. add go to your Profile ( at My Profile Page )
7. There you should see the new purchased product availabel for you
### Buy A Product
1. You must first create a Stripe account -> go to my products page
2. Press the "Create Stripe Account" button
3. make sure you fill all the necessary fields ( Don't have to be your real info )


## Deployment

--Come soon--

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.messages import get_messages



# Sign-in View
def signin(request):
    return render(request, "Authentication/signin.html")


# Sign-up View
def signup(request):
    # Clear previous messages when page is loaded
    storage = get_messages(request)
    for _ in storage:
        pass  # Clears messages when page refreshes

    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass1', '').strip()
        confirm_password = request.POST.get('pass2', '').strip()

        # Check if fields are empty
        if not email or not password or not confirm_password:
            messages.warning(request, "All fields are required.")
            return render(request, "Authentication/signup.html")

        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Passwords don't match.")
            return render(request, "Authentication/signup.html")

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.info(request, "Username/Email already exists.")
            return render(request, "Authentication/signup.html")

        # Create user (inactive until activated)
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        # Email details
        email_subject = "Greetings from Chaithanya - Activate Your Account"
        message = render_to_string("Authentication/activate.html", {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'domain': "yourdomain.com",  # Replace with actual domain
        })

        try:

            # Send activation email
            email_message = EmailMessage(
                subject=email_subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            email_message.content_subtype = "html"  # Ensure email is sent as HTML
            email_message.send()

            messages.success(request, "Account created successfully! Click the link in your email to activate.")
        except Exception as e:
            messages.error(request, f"Error sending activation email: {str(e)}")

        return redirect("/auth/login/")

    return render(request, "Authentication/signup.html")


# Activate Account View
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated Successfully!")
            return redirect("/auth/login/")

        messages.error(request, "Activation link is invalid or expired.")
        return render(request, "Authentication/activatefail.html")


# Login View
def login(request):
    return render(request, "Authentication/login.html")


# Logout View
def logout(request):
    return redirect("/auth/login/")

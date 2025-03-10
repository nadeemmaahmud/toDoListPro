from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from . forms import UserUpdateForm, UserRegisterForm, ContactForm

User = get_user_model()

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully...')
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'user/user_profile.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully...')
    return redirect('user_login')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully...')
                return redirect('todo')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('user_login')
    else:
        form = AuthenticationForm()

    return render(request, 'user/user_login_register.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verification_url = request.build_absolute_uri(
                reverse("verify_email", kwargs={"uidb64": uid, "token": token})
            )

            subject = "Verify Your Email"
            message = f"Hello {user.username},\n\nClick the link below to verify your email:\n{verification_url}\n\nThank you!"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'You have been registered successfully. Please verify your email to continue...')
            return redirect('todo')
    else:
        form = UserRegisterForm()

    return render(request, 'user/user_login_register.html', {'form': form, 'create': True})

def verify_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate user account
        user.save()
        messages.success(request, "Your email has been verified! You can now log in.")
        return redirect("user_login")
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("user_register")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully...')
            return redirect('user_profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/change_reset_password.html', {'form': form, 'update': True})

def reset_password_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
            except MultipleObjectsReturned:
                user = User.objects.filter(email=email).first()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Password Reset'
            message = f"Click the link to reset your password: {reset_url}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, "Your password reset mail is just sent...")
            return redirect('reset_password_request')
    else:
        form = PasswordResetForm()

    return render(request, 'user/change_reset_password.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Your password is reset...")
                return redirect('user_login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'user/change_reset_password.html', {'form': form, 'reset': True})
    else:
        messages.error(request, "The password reset link is invalid or has expired...")
        return redirect('reset_password_request')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            email_message = EmailMessage(
                subject = subject,
                body = message,
                from_email = settings.EMAIL_HOST_USER,
                to = [settings.EMAIL_HOST_USER],
                reply_to = [email],
            )

            email_message.send(fail_silently=False)

            messages.success(request, 'Your message has been sent...')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'user/contact.html', {'form': form})

def about(request):
    return render(request, 'user/about.html')
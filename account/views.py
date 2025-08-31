from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from ProductService.forms import (LoginForm, RegisterForm, ListingSearchForm, ListingCreateForm,
                                    ProductImagesCreateFormSet, ListingUpdateForm, ProductImagesUpdateFormSet)
from orders.models import Order


# Create your views here.
class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        form = LoginForm(request.GET or None)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Wrong username or password!')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogoutView(View):
    template_name = 'account/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect('home')


class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request):
        form = RegisterForm(request.GET or None)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)

        context = {
            'form': form,
        }

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.save()
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, context)

class ProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        user = request.user
        user_orders = Order.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(user_orders, 4)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'user': user,
            'user_orders': page_obj
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        user = request.user

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        photo = request.FILES.get("photo")

        errors = []
        if not first_name:
            errors.append("First name cannot be empty.")
        if not last_name:
            errors.append("Last name cannot be empty.")
        if email and "@" not in email:
            errors.append("Invalid email address.")
        if phone and not phone.startswith("+") and not phone[1:].isdigit():
            errors.append("Phone must start with '+' and contain digits only.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name, {'user': user})

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone
        if photo:
            user.photo = photo
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
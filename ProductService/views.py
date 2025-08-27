from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import View
from ProductService.forms import LoginForm, RegisterForm
from django.core.paginator import Paginator
from django.views.generic import View
from ProductService.forms import LoginForm, RegisterForm, ListingSearchForm, ListingCreateForm, ProductImagesFormSet
from ProductService.models import Listing

# Create your views here.
class HomePageView(View):
    template_name = 'product_service/app/home.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'product_service/account/login.html'

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
    template_name = 'product_service/account/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect('home')


class RegisterView(View):
    template_name = 'product_service/account/register.html'

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


class ListingSearchView(View):
    template_name = 'product_service//app//listing_search.html'

    def get(self, req):
            form = ListingSearchForm(req.GET or None)
            listings = Listing.objects.all()

            if form.is_valid():
                form_data = form.cleaned_data
                name = form_data.get('name')
                max_price = form_data.get('max_price')
                categories = form_data.get('category')

                if name:
                    listings = listings.filter(product_name__icontains=name)
                if max_price:
                    listings = listings.filter(cost__lte=max_price)
                if categories:
                    listings = listings.filter(category__in=categories)

            paginator = Paginator(listings, 10)
            page_number = req.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            return render(req, self.template_name, context={'form': form, 'listings': listings, 'page_obj': page_obj})

class ListingCreateView(LoginRequiredMixin, View):
    template_name = 'product_service/app/listing_create.html'

    def get(self, req):
        listing_form = ListingCreateForm()
        images_form = ProductImagesFormSet()
        context={
            'listing_form': listing_form,
            'images_form': images_form
        }
        return render(req, self.template_name, context)

    def post(self, req):
        listing_form = ListingCreateForm(req.POST)
        images_form = ProductImagesFormSet(req.POST, req.FILES)

        if listing_form.is_valid():
            listing_form.instance.user = req.user
            listing = listing_form.save()
            images_form = ProductImagesFormSet(req.POST, req.FILES, instance=listing)
            if images_form.is_valid():
                images_form.save()
                messages.success(req, 'Listing created successfully!')
                return redirect(reverse('listing-search'))
            else:
                messages.error(req, 'Please add correct images to listing!')
                context = {
                    'listing_form': listing_form,
                    'images_form': images_form
                }
                return render(req, self.template_name, context)

        messages.error(req, 'Please add correct information to listing form')
        context = {
            'listing_form': listing_form,
            'images_form': images_form
        }

        return render(req, self.template_name, context)

class ProfileView(View):
    template_name = 'product_service/account/profile.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user': user})

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


class ListingDetailView(View):
    template_name = 'product_service/app/listing_details.html'

    def get(self, req, **kwargs):
        pk = req.resolver_match.kwargs['pk']
        listing = get_object_or_404(Listing, pk=pk)

        images = listing.product_images.all()
        main_image = images[0]
        context={
            'listing': listing,
            'main_image': main_image,
            'additional_images': images
        }
        return render(req, self.template_name, context=context)
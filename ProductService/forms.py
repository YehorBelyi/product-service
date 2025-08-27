from django import forms
from django.contrib.auth.models import User
from ProductService.models import CustomUser
from ProductService.models import CustomUser, ProductCategory, Listing, ProductImages
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+38\d{10}$',
    message="Your phone must begin from +38 and contain 10 numbers after."
)

email_validator = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message="Enter a valid email address."
)


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        # min_length=8
    )

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    email = forms.CharField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
        validators=[email_validator],
    )
    phone = forms.CharField(
        label="Phone",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380123456789'}),
        validators=[phone_validator],
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

        def clean_username(self):
            username = self.cleaned_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError("User with this username already exists!")
            return username


class ListingSearchForm(forms.Form):
    name = forms.CharField(
        label = "Product name",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Product name',
            'autocomplete': 'off'
        })
    )
    max_price = forms.DecimalField(
        label = "Maximum product price",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Up to'
        })
    )
    category = forms.ModelChoiceField(
        label="Product category",
        required=False,
        queryset=ProductCategory.objects.all(),
        empty_label="None",
        widget=forms.Select(attrs={
            'class': 'dropdown form-select'
        })
    )

class ListingCreateForm(forms.ModelForm):
    product_name = forms.CharField(
        label='Product name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'listing-create-name',
            'placeholder': 'Enter product name'
        })
    )
    product_desc = forms.CharField(
        label='Product description',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'listing-create-desc',
            'placeholder': 'Enter product description'
        })
    )
    category = forms.ModelChoiceField(
        label='Product Category',
        queryset=ProductCategory.objects.all(),
        widget=forms.Select(attrs={
            'class': 'listing-create-categories'
        })
    )
    cost = forms.DecimalField(
        label='Product price',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'listing-create-price',
            'placeholder': 'Price'
        })
    )
    stock = forms.IntegerField(
        label='Product stock quantity',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'listing-create-stock',
            'placeholder': 'Stock quantity'
        })
    )

    class Meta:
        model = Listing
        fields = ['product_name', 'product_desc', 'category', 'cost', 'stock']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (max 5MB).")
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File must be an image.")
        return image

ProductImagesFormSet = forms.inlineformset_factory(
    Listing,
    ProductImages,
    fields=['image'],
    extra=3,
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'listing-create-image',
            'accept': 'image/*'
        })
    }
)

from django import forms
from django.contrib.auth.models import User
from ProductService.models import CustomUser
from ProductService.models import CustomUser, ProductCategory
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
            'class': 'search-name-input',
            'placeholder': 'Product name',
            'autocomplet': 'off'
        })
    )
    max_price = forms.DecimalField(
        label = "Maximum product price",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'search-price-input',
            'placeholder': 'Up to'
        })
    )
    category = forms.MultipleChoiceField(
        label="Product category",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'search-categories-input'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(category.name, category.name) for category in ProductCategory.objects.all()]
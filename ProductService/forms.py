from django import forms
from django.contrib.auth.models import User
from ProductService.models import CustomUser
from ProductService.models import CustomUser, ProductCategory, Listing, ProductImages
from django.core.validators import RegexValidator
from django.core.files.uploadedfile import UploadedFile

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
        queryset=ProductCategory.objects.all().order_by('name'),
        empty_label="None",
        widget=forms.Select(attrs={
            'class': 'dropdown form-select'
        })
    )
    price_order_by = forms.ChoiceField(
        label="Price ordering",
        required=False,
        choices=[('', 'None'),('-cost', 'High to Low'),('cost', 'Low to High')],
        widget=forms.Select(attrs={
            'class': 'dropdown form-select'
        })
    )

class ListingCreateForm(forms.ModelForm):
    product_name = forms.CharField(
        label='Product name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control create-input',
            'placeholder': 'Enter product name'
        })
    )
    product_desc = forms.CharField(
        label='Product description',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product description'
        })
    )
    category = forms.ModelChoiceField(
        label='Product Category',
        queryset=ProductCategory.objects.all(),
        widget=forms.Select(attrs={
            'class': 'dropdown form-select create-input'
        })
    )
    cost = forms.DecimalField(
        label='Product price',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control create-input',
            'placeholder': 'Price'
        })
    )

    class Meta:
        model = Listing
        fields = ['product_name', 'product_desc', 'category', 'cost']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']
        exclude = ['id']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image and isinstance(image, UploadedFile):
            if image.size > 5 * 1024 * 1024:
                print(f"Image size: {image.size}, content_type: {image.content_type}")
                raise forms.ValidationError("Image file too large (max 5MB).")
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File must be an image.")

        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

ProductImagesCreateFormSet = forms.inlineformset_factory(
    Listing,
    ProductImages,
    form=ProductImageForm,
    fields=['image'],
    extra=3,
    min_num=0,
    validate_min=False,
    can_delete=False,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    }
)

ProductImagesUpdateFormSet = forms.inlineformset_factory(
    Listing,
    ProductImages,
    form=ProductImageForm,
    fields=['image'],
    extra=0,
    can_delete=False,
    min_num=0,
    validate_min=False,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'listing-create-image',
            'accept': 'image/*'
        })
    }
)


class ListingUpdateForm(forms.ModelForm):
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

    class Meta:
        model = Listing
        fields = ['product_name', 'product_desc', 'category', 'cost']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['product_name'].initial = instance.product_name
            self.fields['product_desc'].initial = instance.product_desc
            self.fields['category'].initial = instance.category
            self.fields['cost'].initial = instance.cost
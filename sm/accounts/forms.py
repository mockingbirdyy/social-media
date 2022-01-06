from django import forms
from .models import Profile

login_messages = {
    'invalid': 'معتبر نیست',
    'required': 'این فیلد اجباری است'
}

register_messages = {
    'invalid': 'لطفا یک ایمیل معتبر وارد کنید',
    'required': 'این فیلد اجباری است'
}


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, error_messages=login_messages, widget=forms.TextInput(attrs={'class': 'form-control mt-3 mb-4 ', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=50, error_messages=login_messages, widget=forms.PasswordInput(attrs={'class': 'form-control  mt-4 mb-3 ', 'placeholder': 'Password'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, error_messages=register_messages, widget=forms.TextInput(attrs={'class': 'form-control mt-3 mb-4', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=70, error_messages=register_messages, widget=forms.EmailInput(attrs={'class': 'form-control mt-4 mb-3', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, error_messages=register_messages, widget=forms.PasswordInput(attrs={'class': 'form-control mt-4 mb-3', 'placeholder': 'Password'}))


class EditProfile(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control  mt-4 mb-4', 'placeholder': 'Email'}))

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'phone')
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control mt-4 mb-4', 'placeholder': 'Bio'}),
            'age': forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Age'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'phone number'}),
        }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'phone number'}))

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('this phone number does not exists')
        return self.cleaned_data['phone']

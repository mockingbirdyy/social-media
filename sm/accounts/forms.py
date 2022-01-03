from django import forms


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
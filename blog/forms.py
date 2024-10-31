from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
    name = forms.CharField(required=True, max_length=250, label="Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=11, required=True, label="Phone")
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="Subject")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن عددی نیست')
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError('نام کوتاه است')
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label=' تصویر اول', required=False)
    image2 = forms.ImageField(label='تصویر دوم', required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']


# class LoginForm(forms.Form):
#    username = forms.CharField(max_length=250, required=True)
#    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=250, widget=forms.PasswordInput, required=True, label='password')
    password2 = forms.CharField(max_length=250, widget=forms.PasswordInput, required=True, label='repeat password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("رمز ها مطابقت ندارند!")
        return cd['password2']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']

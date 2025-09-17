# section for creating forms related to CustomUser

# widgets for customizing form inputs
# we can use widgets to change how fields are displayed:
# widgets = {
            # 'active_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter activation code'})
        # }

# for serializers we use extra_kwargs

# labels for changing field names
# display names of fields can be changed:
# labels = {
#             'active_code': 'Activation code'
#         }

# help_texts for user guidance
# if you want to show an explanation under the field:
# help_texts = {
            # 'active_code': 'Enter the 6-digit code sent to your number.'
        # }

# __init__ for customizing form during initialization
# default values of fields can be set:
# def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['active_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter received code'})

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class UserCreationForm(ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="RePassword",widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['mobile_number','email','name','family','gender']
    
    # to apply conditions to fields and check them we use this function
    # def clean(self) -> dict[str, Any]:
    #     return super().clean()
  
    # if I only want to check password2 field, I use clean like this
    # self, is the form content that we have access to.
    # for validation in forms.
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Password and its repetition do not match")
        return pass2
    
    # rewriting the save function for modelforms
    # commit means final confirmation. and when it happens it will be saved.
    # if I don't rewrite this save, password will be saved without hashing with other data.
    def save(self,commit=True):
        # commit false causes user not to be saved and we put the unsaved user in user
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

from django.contrib.auth.forms import ReadOnlyPasswordHashField

# I want the password that I change here to be hashed again.
class UserChangeForm(ModelForm):
    # this causes the password in our change form to be read only.
    # adding to the related message about password user related in admin panel.
    password  = ReadOnlyPasswordHashField(help_text="To change password click on this <a href='../password'>link</a>")
    class Meta:
        model = CustomUser
        fields = ['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
        

# now we need to add these forms to the admin panel.     

# ---------------------------------------------------------------------------------------------

# first step in creating form for usual user that don't normally access or use admin pannel though the model is the same.

class RegisterUserForm(ModelForm):
    # since password field is defined from form type, here in forms we give it the label.
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'}))
    password2 = forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repeat password'}))
    class Meta:
        model = CustomUser
        # since mobile field is defined from model type, here in model we give it the verbose_name.
        fields = ["mobile_number",]
        widgets = {
            "mobile_number" : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number'}),
        }
        
    def clean_password(self):
        pass1 = self.cleaned_data["passwprd1"]
        pass2 = self.cleaned_data["password2"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Password and its repetition do not match")
        return pass2
        
        
# ----------------------------------------------------------------------------------------------------------------------
        
# In the error_messages field you can customize different error messages for different types of validation errors. except required
# invalid
# when the input value is not valid, this message is displayed.
# max_length
# when the input value is more than max_length, this message is displayed.
# min_length
# when the input value is less than min_length, this message is displayed.
# max_value and min_value (for numeric fields)
# used for values exceeding the allowed limit or less than the allowed value.
# unique (in ModelForm)
# if the entered value already exists in the database, this error is displayed.

class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',error_messages={"required":"This field cannot be empty"},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter received code'}))      
        
        
# ----------------------------------------------------------------------------------------------------------------------
        
# creating a form for a user who has registered and now wants to login.
# does not depend on a specific model.

# if we write something in the label here, it will be added to the HTML label tag
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(max_length=11,label="Mobile",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your mobile number'}))
        
    password = forms.CharField(label="Password",error_messages={"required":"This field cannot be empty!"},widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' Enter your password'}))
    
# ------------------------------------------------------------------------------
            
# before Changing Password:
# we need a phone_number in this form and send user to an other page

class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label="Mobile",error_messages={'required':'Mobile number is required'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your mobile number'}))

# ------------------------------------------------------------------------------



class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="Password",
                                error_messages={"required":"This field cannot be empty!"},
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' Enter your password'}))
    
    password2 = forms.CharField(label="Password",
                                error_messages={"required":"This field cannot be empty!"},
                                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' Repeat your password'}))
    
    def clean_password(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password1']
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Password and its repetition are not the same")
        return pass2
    
    
# ------------------------------------------------------------------------------

# readonly : we give to a field that we don't want the user to change
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your mobile number','readonly':'readonly'}), error_messages={"required":"This field cannot be empty!"})
    
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}), error_messages={"required":"This field cannot be empty!"})
    
    family = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your family name'}), error_messages={"required":"This field cannot be empty!"})
    
    phone_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your landline number'}), error_messages={"required":"This field cannot be empty!"})
    
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),required=False)
    
    
    address = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your address'}), error_messages={"required":"This field cannot be empty!"})
    
    
    image = forms.ImageField(label="",required=False)
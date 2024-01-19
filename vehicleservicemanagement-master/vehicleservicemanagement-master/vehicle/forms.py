from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']


class MechanicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MechanicForm(forms.ModelForm):
    class Meta:
        model=models.Mechanic
        fields=['address','mobile','profile_pic','skill']

class MechanicSalaryForm(forms.Form):
    salary=forms.IntegerField();



class RequestForm(forms.Form):
    projectInformation = forms.CharField(label='Project Information',widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    startDate = forms.DateField(label='Start Date',widget=forms.DateInput(attrs={'class': 'form-input'}, format='%Y-%m-%d'),required=True)
    endDate = forms.DateField(label='End Date',widget=forms.DateInput(attrs={'class': 'form-input'}, format='%Y-%m-%d'), required=True)
    workLocation = forms.CharField(label='Work Location', widget=forms.TextInput(attrs={'class': 'form-input'}),required=True)
    domain = forms.CharField(label='Select Domain', widget=forms.Select(attrs={'class': 'form-input'}), required=True)
    roleName = forms.CharField(label='Select Role', widget=forms.Select(attrs={'class': 'form-input'}), required=True)
    experienceLevel = forms.ChoiceField(label='Experience Level', widget=forms.Select(attrs={'class': 'form-input'}),choices=[('', 'Select Experience Level'), ('Entry Level', 'Entry Level'),('Mid Level', 'Mid Level'), ('Senior Level', 'Senior Level')],required=True)
    technology = forms.CharField(label='Technology', widget=forms.TextInput(attrs={'class': 'form-input'}),required=True)
    skill = forms.CharField(label='Skills', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
class AdminRequestForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    customer=forms.ModelChoiceField(queryset=models.Customer.objects.all(),empty_label="Customer Name",to_field_name='id')
    mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    cost=forms.IntegerField()

class AdminApproveRequestForm(forms.Form):
    mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    cost=forms.IntegerField()
    stat=(('Pending','Pending'),('Approved','Approved'),('Released','Released'))
    status=forms.ChoiceField( choices=stat)


class UpdateCostForm(forms.Form):
    cost=forms.IntegerField()

class MechanicUpdateStatusForm(forms.Form):
    stat=(('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'))
    status=forms.ChoiceField( choices=stat)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['by','message']
        widgets = {
        'message':forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

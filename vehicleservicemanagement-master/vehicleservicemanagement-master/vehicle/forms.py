from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['email','mobile','profile_pic']



class RequestForm(forms.Form):
    projectInformation = forms.CharField(label='Project Information', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    startDate = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'class': 'form-input'}, format='%Y-%m-%d'), required=True)
    endDate = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'class': 'form-input'}, format='%Y-%m-%d'), required=True)
    workLocation = forms.CharField(label='Work Location', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    masterAgreementType = forms.ChoiceField(label='Select Master Agreements', widget=forms.Select(attrs={'class': 'form-input'}), choices=[], required=True)
    domain = forms.CharField(label='Select Domain', widget=forms.Select(attrs={'class': 'form-input'}), required=True)
    roleName = forms.CharField(label='Select Role', widget=forms.Select(attrs={'class': 'form-input'}), required=True)
    experienceLevel = forms.ChoiceField(label='Experience Level', widget=forms.Select(attrs={'class': 'form-input'}), choices=[('', 'Select Experience Level'), ('Entry Level', 'Entry Level'), ('Mid Level', 'Mid Level'), ('Senior Level', 'Senior Level')], required=True)
    technology = forms.CharField(label='Technology', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    skill = forms.CharField(label='Skills', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)

    def clean_masterAgreementType(self):
        # Get the raw value
        master_agreement_type = self.cleaned_data.get('masterAgreementType', '')

        return f'MAT{master_agreement_type}'

    @classmethod
    def set_api_data(cls, api_data):
        choices = [(str(item['masterAgreementTypeId']), item['masterAgreementTypeName']) for item in api_data]
        cls.base_fields['masterAgreementType'].choices = choices
        cls.declared_fields['masterAgreementType'].choices = choices

        # Set choices for domain field
        domain_choices = [(str(domain['id']), domain['domainName']) for item in api_data for domain in item.get('domains', [])]
        cls.base_fields['domain'].choices = domain_choices
        cls.declared_fields['domain'].choices = domain_choices





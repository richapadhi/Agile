from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages  # Import the messages module

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
import json
from .models import Request
from django.http import JsonResponse


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'vehicle/index.html')

# for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'vehicle/customerclick.html')

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm, 'error_message': ''}

    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)

        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.email = userForm.cleaned_data.get('email')  # Ensure email is set
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)

            # External API call
            api_url = "http://codexauthv2.onrender.com/api/register/"
            api_data = {
                "username": user.username,
                "email": user.email,
                "password": request.POST.get('password'),
                "role": "Base User",
                "provider": "Team 4a"
            }

            response = requests.post(api_url, json=api_data)
            print(response)

            if response.status_code == 200 or 201:
                response_data = response.json()
                print(response_data)
                token = response_data.get("token")
                print(token)
                request.session['api_token'] = token
                # Save the token as needed
            else:
                if response.status_code == 500:
                    print("Username already exists or invalid data sent.")  # Debugging line
                    messages.error(request, 'Username already exists or invalid data sent.')
                elif response.status_code == 400:
                    messages.error(request, 'Server error occurred during registration')
                else:
                    messages.error(request, 'An unknown error occurred during registration.')

                return render(request, 'vehicle/customersignup.html', context=mydict)

            return HttpResponseRedirect('customerlogin')

    return render(request, 'vehicle/customersignup.html', context=mydict)

def customer_login_view(request):
    # Initialize the form for a GET request
    form = AuthenticationForm()

    if request.method == 'POST':
        print("Processing a POST request")  # Debugging print

        # Process the form data for a POST request
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Form is valid. Username: {username}, Password: {password}")  # Debugging print

            # External API call
            api_response = requests.post('http://codexauthv2.onrender.com/api/login/', data={'username': username, 'password': password})
            print(f"API response status code: {api_response.status_code}")  # Debugging print

            if api_response.status_code == 200:
                # Authenticate the user on the Django side
                user = authenticate(request, username=username, password=password)
                print(f"User from authenticate: {user}")  # Debugging print

                if user is not None:
                    login(request, user)
                    print("User authenticated and logged in, redirecting to dashboard")  # Debugging print
                    return redirect('customer-dashboard')
                else:
                    print("User authentication failed")  # Debugging print
                    messages.error(request, 'User does not exist in the local database')
            else:
                print("API login failed")  # Debugging print
                messages.error(request, 'Login failed with the external API')
        else:
            print("Form is invalid")  # Debugging print
            messages.error(request, 'Invalid username or password')

    # Render the login form for both GET requests and failed POST requests
    print("Rendering customer login form")  # Debugging print
    return render(request, 'vehicle/customerlogin.html', {'form': form})
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')


# ============================================================================================
# CUSTOMER RELATED views start
# ============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/customer_dashboard.html')


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/customer_dashboard.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)

    # Initialize 'enquiries'
    enquiries = []

    # API URL
    api_url = 'http://ec2-54-166-224-107.compute-1.amazonaws.com:9198/api/v1/serviceManagement'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            enquiries = response.json()
            print("Fetched enquiries:", enquiries)  # Debug print
        else:
            print("Failed to fetch data from API")
    except requests.RequestException as e:
        print("Request failed: ", e)

    return render(request, 'vehicle/customer_view_request.html', {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request, pk):
    # Retrieve the enquiry to be deleted
    try:
        enquiry = Request.objects.get(pk=pk)
        # Check if the user has the permission to delete this enquiry (e.g., ownership check)
        if enquiry.customer.user_id == request.user.id:
            enquiry.delete()  # Delete the enquiry from the database
        else:
            # Handle the case where the user doesn't have permission to delete this enquiry
            return render(request, 'vehicle/error.html')
    except Request.DoesNotExist:
        # Handle the case where the enquiry with the given primary key doesn't exist
        return render(request, 'vehicle/error.html')

    # Redirect back to the 'customer-view-request' page after successful deletion
    return redirect('customer-view-request')


@login_required(login_url='customerlogin')
@require_http_methods(["DELETE"])
def delete_service(request, service_id):
    try:
        service = Request.objects.get(service_id=service_id)
        service.delete()
        return JsonResponse({'message': 'Service deleted successfully'}, status=200)
    except Request.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    all_offers_url = 'http://ec2-54-166-224-107.compute-1.amazonaws.com:9198/api/v1/serviceManagement'
    specific_offers_url = 'https://agiledev3a.pythonanywhere.com/p3aplatform/api/service_offers'

    # Fetch all offers
    response = requests.get(all_offers_url)
    offers = response.json() if response.status_code == 200 else []
    print(offers)

    selected_service_id = request.GET.get('service_id')
    specific_offers = []

    if selected_service_id:
        # Fetch offers for specific service ID
        response = requests.get(specific_offers_url)
        if response.status_code == 200:
            all_specific_offers = response.json()
            # Filter offers for the selected service ID
            specific_offers = [offer for offer in all_specific_offers if offer['serviceId'] == int(selected_service_id)]
            print("specific_offers:", specific_offers)
    return render(request, 'vehicle/customer_view_approved_request.html', {
        'offers': offers,
        'specific_offers': specific_offers,
        'selected_service_id': selected_service_id
    })


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request, 'vehicle/customer_view_approved_request_invoice.html',
                  {'customer': customer, 'enquiries': enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    api_url = 'http://ec2-13-49-44-175.eu-north-1.compute.amazonaws.com:5000/api/mastertype/all'

    # Make a request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        api_data = response.json()
        domain_names = []
        roleName = []
        exp_level = []
        technologyCatalog = []

        for master_agreement in api_data:
            for domain in master_agreement.get('domains', []):
                domain_names.append({'id': domain.get('id', ''), 'domainName': domain.get('domainName', '')})
                # domain_names.append(domain.get('domainName', ''))
                for role in domain.get('roles', []):
                    roleName.append(role.get('roleName', ''))

        context = {'domain_names': domain_names, 'roleName': roleName, 'master_agreements': api_data}
        forms.RequestForm.set_api_data(api_data)
        enquiry = forms.RequestForm()
    else:
        context = {'domain_names': None, 'roleName': None, 'master_agreements': None}

    customer = models.Customer.objects.get(user_id=request.user.id)
    # enquiry = forms.RequestForm()

    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        if enquiry.is_valid():
            project_information = enquiry.cleaned_data['projectInformation']
            start_date = enquiry.cleaned_data['startDate']
            end_date = enquiry.cleaned_data['endDate']
            work_location = enquiry.cleaned_data['workLocation']
            master_agreement_type = enquiry.cleaned_data['masterAgreementType']
            # Debug prints
            print("Selected Domain ID:", enquiry.cleaned_data['domain'])
            print("Selected Role Name:", enquiry.cleaned_data['roleName'])
            print("Selected Master Agreement:", enquiry.cleaned_data['masterAgreementType'])

            domain = enquiry.cleaned_data['domain']
            role = enquiry.cleaned_data['roleName']
            experience_level = enquiry.cleaned_data['experienceLevel']
            technology = enquiry.cleaned_data['technology']
            skill = enquiry.cleaned_data['skill']
            customer = models.Customer.objects.get(user_id=request.user.id)

            # Debug prints
            print("Processed Domain ID:", domain)
            print("Processed Role Name:", role)

            # Prepare data payload
            data = {
                "projectInfo": project_information,
                "startDate": start_date.strftime('%Y-%m-%d'),  # Convert to string
                "endDate": end_date.strftime('%Y-%m-%d'),  # Convert to string
                "workLocation": work_location,
                "masterAgreementName": master_agreement_type,
                "domain": domain,
                "role": role,
                "experience": experience_level,
                "technology": technology,
                "skill": skill,
                # ...
            }

            enquiry_instance = Request(
                projectInformation=project_information,
                startDate=start_date,
                endDate=end_date,
                workLocation=work_location,
                master_agreements=master_agreement_type,
                positionDomain=domain,
                positionRole=role,
                experienceLevel=experience_level,
                technology=technology,
                skill=skill,
                customer=customer  # Assuming customer is a foreign key field
            )
            enquiry_instance.save()

            # Make a POST request to the API
            api_endpoint = "http://ec2-54-166-224-107.compute-1.amazonaws.com:9198/api/v1/serviceManagement"  # Update with your API endpoint
            # response = requests.post(api_endpoint, data=data)
            # Convert data to JSON format
            json_data = json.dumps(data)
            print(json_data)

            # Set the Content-Type header to indicate JSON data
            headers = {'Content-Type': 'application/json'}

            # Make a POST request to the API with JSON data
            response = requests.post(api_endpoint, data=json_data, headers=headers)
            print("status code:", response.status_code)
            if response.status_code in [200, 201]:
                return HttpResponseRedirect('customer-view-request')
            else:
                return render(request, 'vehicle/error.html')
        else:
            print("form is invalid")
            print(enquiry.errors)
        return HttpResponseRedirect('customer-dashboard')
    return render(request, 'vehicle/customer_add_request.html',
                  {'enquiry': enquiry, 'customer': customer, 'domain_names': domain_names, 'roleName': roleName})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'vehicle/customer_profile.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm, 'customer': customer}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request, 'vehicle/edit_customer_profile.html', context=mydict)

# ============================================================================================
# CUSTOMER RELATED views END
# ============================================================================================

# for aboutus
def aboutus_view(request):
    return render(request, 'vehicle/aboutus.html')




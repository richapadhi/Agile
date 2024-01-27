"""
vehicle
"""
from django.contrib import admin
from django.urls import path
from vehicle import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
#from vehicle.views import delete_enquiry
class LogoutViewWithGet(LogoutView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('customerclick', views.customerclick_view),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', views.customer_login_view, name='customerlogin'),

    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),

    path('customer-view-request/',views.customer_view_request_view,name='customer-view-request'),

    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),
    path('api/v1/serviceManagement/<int:service_id>', views.delete_service, name='delete_service'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='vehicle/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),

]

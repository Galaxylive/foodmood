from django.contrib import admin

from django.conf.urls import url, include
from django.urls import path

from django.urls import reverse

from foodtaskerapp import views, apis

from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home ,name='home'),

    #restaurent
    path('restaurent/sign-in/',
        LoginView.as_view(template_name='restaurent/sign_in.html'),
        name="restaurent-sign-in"),
    path('restaurent/sign-out/',LogoutView.as_view(next_page ='/'),
        name="restaurent-sign-out"),
    path('restaurent/sign-up/',views.restaurent_sign_up,name="restaurent-sign-up"),
    path('restaurent/',views.restaurent_home,name = 'restaurent-home'),
    path('restaurent/account/', views.restaurent_account, name = 'restaurent-account'),
    path('restaurent/meal/', views.restaurent_meal, name = 'restaurent-meal'),
    path('restaurent/meal/add/', views.restaurent_add_meal, name = 'restaurent-add-meal'),
    path('restaurent/meal/edit/<meal_id>/', views.restaurent_edit_meal, name = 'restaurent-edit-meal'),
    path('restaurent/order/', views.restaurent_order, name = 'restaurent-order'),
    path('restaurent/report/', views.restaurent_report, name = 'restaurent-report'),

    #social authenticate sign in/sign up/sign out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/sign up)
    # /revoke-token (sign out)

    path('api/restaurent/order/notification/<str:last_request_time>/', apis.restaurent_order_notification),

    #APIs for CUSTOMERS
    path('api/customer/restaurents/',apis.customer_get_restaurents),
    path('api/customer/meals/<restaurent_id>/',apis.customer_get_meals),
    path('api/customer/order/add/',apis.customer_add_orders),
    path('api/customer/order/latest/',apis.customer_get_latest_orders),

    #APIs for DRIVER
    path('api/driver/orders/ready/', apis.driver_get_ready_orders),
    path('api/driver/order/pick/', apis.driver_pick_orders),
    path('api/driver/order/latest/', apis.driver_get_latest__orders),
    path('api/driver/order/complete/', apis.driver_complete_orders),
    path('api/driver/revenue/', apis.driver_get_revenue),



] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

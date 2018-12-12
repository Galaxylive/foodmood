from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from foodtaskerapp import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home ,name='home'),
    # url(r'^restaurent/sign-in/$',LoginView,
    #     {'template_name': 'restaurent/sign_in.html'},
    #     name = 'restaurent-sign-in'),
    # url(r'^restaurent/sign-out/$',logout,
    #     {'next_page': '/'},
    #     name = 'restaurent-sign-out' ),
    path('restaurent/sign-in/',
        LoginView.as_view(template_name='restaurent/sign_in.html'),
        name="restaurent-sign-in"),
    path('restaurent/sign-out/',
        LogoutView.as_view(next_page ='/'),
        name="restaurent-sign-out"),
    path('restaurent/sign-up/',
        views.restaurent_sign_up,
        name="restaurent-sign-up"),
    path('restaurent/',views.restaurent_home,name = 'restaurent-home'),
] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

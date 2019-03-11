from django.conf.urls import url
from controls.views import controls, search, controls2_data, controls2_allot, \
    controls1_submit, sync_db, search3, controls3_submit
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'sync_db/$', sync_db, name='sync_db'),
    url(r'controls/$', controls, name='controls'),
    url(r'controls1_submit/$', controls1_submit, name='controls1_submit'),
    url(r'search/$', search, name='search'),
    url(r'controls2_data/$', controls2_data, name='controls2_data'),
    url(r'controls2_allot/$', controls2_allot, name='controls2_allot'),
    url(r'controls3_submit/$', controls3_submit, name='controls3_submit'),

    url(r'search3/$', search3, name='search3'),
    # url(r'controls3_allot/$', controls3_allot, name='controls3_allot'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(), name='logout'),
    url(r'$',
        auth_views.LoginView.as_view(
            template_name='controls/index.html',
            redirect_authenticated_user=True), name='login'),
    ]

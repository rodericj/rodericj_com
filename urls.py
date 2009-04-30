from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^rodericj_com/', include('rodericj_com.foo.urls')),

    # Uncomment this for admin:
     (r'^callme/', include('rodericj_com.callme.urls')),
     (r'^accounts/login/', 'django.contrib.auth.views.login'),
     #(r'^callme/admin/', include('django.contrib.admin.urls')),
     #(r'^callme/create/', 'rodericj_com.callme.views.create'),
     #(r'^callme/action/', 'rodericj_com.callme.views.action'),
	
)

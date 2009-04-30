from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^rodericj_com/', include('rodericj_com.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'rodericj_com.callme.views.start'),
     (r'^create/', 'rodericj_com.callme.views.create'),
     (r'^createaccount/', 'rodericj_com.callme.views.createaccount'),
     (r'^login/', 'rodericj_com.callme.views.Clogin'),
     (r'^logout/', 'rodericj_com.callme.views.logout_view'),
     (r'^action/', 'rodericj_com.callme.views.action'),
     (r'^newaction/', 'rodericj_com.callme.views.newaction'),
	
)

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^rodericj_com/', include('rodericj_com.foo.urls')),

    # Uncomment this for admin:
     #(r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'callme.views.start'),
     (r'^createprofile/', 'callme.views.createprofile'),
     (r'^create/', 'callme.views.create'),
     (r'^newaction/', 'callme.views.newaction'),
     (r'^resend/', 'callme.views.resend'),
     (r'^cron/', 'callme.views.cron'),
     #(r'^createaccount/', 'rodericj_com.callme.views.createaccount'),
     #(r'^login/', 'rodericj_com.callme.views.Clogin'),
     (r'^logout/', 'callme.views.logout_view'),
     #(r'^change_password/', 'django.contrib.auth.views.password_change'),
     #(r'^action/', 'rodericj_com.callme.views.action'),
     #(r'^newaction/', 'rodericj_com.callme.views.newaction'),
     #(r'^validate/', 'rodericj_com.callme.views.validate'),
)   

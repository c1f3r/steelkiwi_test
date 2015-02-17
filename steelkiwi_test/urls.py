from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'steelkiwi_test.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^accounts/',
                           include('registration.backends.default.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('mySO.urls')),
                       url('', include('social.apps.django_app.urls',
                                       namespace='social'))

)

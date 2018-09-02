from       django.conf.urls import patterns, include, url
from         django.contrib import admin
from            django.conf import settings
from                 cctool import views
from rest_framework.routers import DefaultRouter


admin.autodiscover()

# A router to register viewsets.
router = DefaultRouter()
router.register( r'users',        views.UserViewSet                       )
router.register( r'graphs',       views.GraphViewSet,      'graph'        )
router.register( r'admingraphs',  views.AdminGraphViewSet, 'admingraph'   )
router.register( r'implications', views.Implications,      'implications' )

urlpatterns = patterns('',
	# include django-rest-framework api_root
	url( r'^api-root/', include(router.urls)                                       ),
	url( r'^api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
	# include django admin sites.
	url( r'^admin/',    include(admin.site.urls)                                   ),
	# include application sites (cctool)
	url( r'^',          include('cctool.urls', namespace="cctool")                 ),
	url( r'^cctool/',   include('cctool.urls', namespace="cctool")                 ),
	# include application static files
	# url( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	# url( r'^dashboard/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),
	# url( r'^app/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[1]}),
)
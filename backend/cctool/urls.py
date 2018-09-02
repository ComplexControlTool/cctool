import os
from django.conf.urls import patterns, include, url
from          cctool  import views
from django.views.generic.base import RedirectView


urlpatterns = patterns('',

	# /cctool/...
	url( r'^$',                           views.HomeView.as_view(),            name='home'            ),
  url( r'^cctool/$',                    views.CCToolView.as_view(),          name='tool'            ),
	url( r'^cctool/graphs$',              views.CCToolView.as_view(),          name='usergraphs'      ),
  url( r'^cctool/graphs/[0-9]+$',       views.CCToolView.as_view(),          name='usergraphs'      ),
  url( r'^cctool/graphs/demo$',         views.CCToolView.as_view(),          name='graphsdemo'      ),
  url( r'^cctool/graphs/demo/[0-9]+$',  views.CCToolView.as_view(),          name='graphsdemo'      ),
  url( r'^cctool/graphs/new$',          views.CCToolView.as_view(),          name='newusergraph'    ),
  url( r'^cctool/graphs/new/import$',   views.CCToolView.as_view(),          name='newimportgraph'  ),
  url( r'^cctool/graphs/new/create$',   views.CCToolView.as_view(),          name='newcreategraph'  ),
  url( r'^cctool/graphs/edit$',         views.CCToolView.as_view(),          name='editusergraph'   ),
  url( r'^cctool/graphs/edit/[0-9]+$',  views.CCToolView.as_view(),          name='updateusergraph' ),
  
  url( r'^cctool/login/$',              views.LoginView.as_view(),           name='login'           ),
  url( r'^cctool/login_auth/$',         views.LoginAuthView.as_view(),       name='loginauth'       ),
  url( r'^cctool/logout/$',             views.LogoutView.as_view(),          name='logout'          ),
  url( r'^cctool/invalid_login/$',      views.InvalidLoginView.as_view(),    name='invalidlogin'    ),
  url( r'^cctool/register/$',           views.RegisterUserView.as_view(),    name='registeruser'    ),
  url( r'^cctool/register_success/$',   views.RegisterSuccessView.as_view(), name='registersuccess' ),

)

mode = os.environ.get('RUN_MODE', '')
if mode != 'prod':
  urlpatterns += url(r'^app/(?P<path>.*)$', RedirectView.as_view(url='/static/cctool/dashboard/app/%(path)s', permanent=True)),
  urlpatterns += url(r'^assets/(?P<path>.*)$', RedirectView.as_view(url='/static/cctool/dashboard/assets/%(path)s', permanent=True)),
  urlpatterns += url(r'^bower_components/(?P<path>.*)$', RedirectView.as_view(url='/static/cctool/dashboard/vendor/%(path)s', permanent=True)),
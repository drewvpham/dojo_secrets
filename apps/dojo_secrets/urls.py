from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^secrets$', views.secrets, name='secrets'),
    url(r'^popular$', views.popular, name='popular'),
    url(r'^logout$', views.logout, name='popular'),
    url(r'^submit_secret$', views.submit_secret, name='submit_secret'),
    url(r"^delete/(?P<find>\d*)", views.delete, name='delete'),
    url(r"^like/(?P<find>\d*)", views.like, name='like'),
    url(r"^unlike/(?P<find>\d*)", views.unlike, name='unlike'),
]

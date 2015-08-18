from django.conf.urls import patterns
from django.conf.urls import url

from record_expungement_webapp import views

urlpatterns = patterns('',
    url(r'^start$', views.start, name='start'),
    url(r'^upload_rap_sheet$', views.upload_rap_sheet, name='upload_rap_sheet'),
    url(r'^complete_personal_info$', views.complete_personal_info, name='complete_personal_info'),
    url(r'^submit_personal_info$', views.submit_personal_info, name='submit_personal_info'),
    url(r'^success$', views.success, name='success'),
    url(r'^download_forms$', views.download_forms, name='download_forms'),
)

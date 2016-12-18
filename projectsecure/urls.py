from django.conf.urls import url, include
from django.contrib import admin

handler400 = 'projectsecure.utils.bad_request'
handler403 = 'projectsecure.utils.permission_denied'
handler404 = 'projectsecure.utils.page_not_found'
handler500 = 'projectsecure.utils.server_error'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/', include('users.urls')),
    url(r'api/', include('challenges.urls')),
    url(r'api/', include('feedback.urls')),
]

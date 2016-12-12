from django.conf.urls import url, include
from django.contrib import admin

handler400 = 'projectsecure.utils.views.bad_request'
handler403 = 'projectsecure.utils.views.permission_denied'
handler404 = 'projectsecure.utils.views.page_not_found'
handler500 = 'projectsecure.utils.views.server_error'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/', include('users.urls')),
    url(r'api/', include('challenges.urls')),
]

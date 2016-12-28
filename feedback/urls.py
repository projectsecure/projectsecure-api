from django.conf.urls import url
from feedback.views import SendFeedbackView

urlpatterns = [
    url(r'^feedback$', SendFeedbackView.as_view(), name='feedback')
]

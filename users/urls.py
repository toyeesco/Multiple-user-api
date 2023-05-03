from django.urls import path
from .views import FreelanceSignupView, ClientSignupView, CustomAuthToken, LogoutView, ClientOnlyView, FreelancerOnlyView

urlpatterns = [
    path('signup/freelancer/', FreelanceSignupView.as_view(), name='freelance-signup'),
    path('signup/client/', ClientSignupView.as_view(), name='client-signup'),
    path('login/', CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', LogoutView.as_view()),
    path('client/dashboard/', ClientOnlyView.as_view()),
    path('freelancer/dashboard/', FreelancerOnlyView.as_view())
]
from django.urls import path
from. import views
urlpatterns = [
    path('',views.homepage,name='homepage' ),
    path('login',views.login_request,name='login_request' ),
    path('logout',views.logout_request,name='logout_request' ),
    path('register',views.signup,name='signup' ),
    path('patienthistory',views.userhistory,name='patienthistory' ),
    path('showpatienthistory',views.showpatienthistory,name='showpatienthistory' ),
    path('medicine',views.medicine,name='medicine' ),
    path('test',views.test,name='test' ),
]
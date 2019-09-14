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
    path('lab',views.test,name='test' ),
    path('showpatientprofile', views.showpatientprofile, name = "patientprofile"),
    path('createcase', views.createcase, name = "createcase"),
    path('existingcase', views.existingcase, name = "existingcase"),
    path('save_medic', views.save_medic, name = "save_medic"),
    path('save_lab', views.save_lab, name = "save_lab"),
    path('save_mediocar', views.save_mediocar, name = "save_mediocar"),
    path('mediocar', views.mediocar, name = "mediocar"),
    path('save_doc', views.save_doc, name = "save_doc"),
    #path('createvisit', views.createvisit, name = "createvisit"),
    
    
]
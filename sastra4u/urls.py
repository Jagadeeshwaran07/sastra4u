from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('register',views.register,name="register"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('check_otp',views.check_otp, name = 'check_otp'),
    path('YourSyllabus',views.YourSyllabus,name = 'YourSyllabus'),
    path('attendance',views.attendance,name = 'attendance'),
    path('gradecalculation',views.gradecalculation,name = 'gradecalculation'),
    path('queries',views.queries,name = 'queries')

]


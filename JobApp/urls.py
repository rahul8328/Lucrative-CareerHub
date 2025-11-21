from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
               path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),	      
               path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
               path("GraduateRegisterAction", views.GraduateRegisterAction, name="GraduateRegisterAction"),
               path("GraduateRegister.html", views.GraduateRegister, name="GraduateRegister"),
               path("CompanyRegisterAction", views.CompanyRegisterAction, name="CompanyRegisterAction"),
               path("CompanyRegister.html", views.CompanyRegister, name="CompanyRegister"),
	       path("GraduateLogin.html", views.GraduateLogin, name="GraduateLogin"),
	       path("GraduateLoginAction", views.GraduateLoginAction, name="GraduateLoginAction"),
	       path("CompanyLogin.html", views.CompanyLogin, name="CompanyLogin"),
               path("CompanyLoginAction", views.CompanyLoginAction, name="CompanyLoginAction"),
	       path("ViewUsers", views.ViewUsers, name="ViewUsers"),
               path("ApproveTeams", views.ApproveTeams, name="ApproveTeams"),	   
	       path("EditProfile", views.EditProfile, name="EditProfile"),
	       path("EditProfileAction", views.EditProfileAction, name="EditProfileAction"),
	       path("CheckTeam", views.CheckTeam, name="CheckTeam"),
	       path("PostProject", views.PostProject, name="PostProject"),
	       path("ApproveTeam", views.ApproveTeam, name="ApproveTeam"),
	       path("PostProjectAction", views.PostProjectAction, name="PostProjectAction"),
	       path("ViewTeam", views.ViewTeam, name="ViewTeam"),	       
	       path("ChooseTeam", views.ChooseTeam, name="ChooseTeam"),
	       path("Download", views.Download, name="Download"),
]

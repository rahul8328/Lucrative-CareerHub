from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pickle
import pymysql
import os
from django.core.files.storage import FileSystemStorage
from datetime import date

global uname

def CheckTeam(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Project ID</th><th><font size="3" color="black">Company Name</th>'
        output+='<th><font size="3" color="black">Application Type</th><th><font size="3" color="black">Project Description</th>'
        output+='<th><font size="3" color="black">Required Skills</th><th><font size="3" color="black">Project Posted Date</th>'
        output+='<th><font size="3" color="blue">Status</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM postproject")
            rows = cur.fetchall()
            for row in rows:
                members = row[6].split(",")
                if uname in members:
                    output+='<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                    output+='<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                    output+='<td><font size="3" color="black">'+str(row[4])+'</td><td><font size="3" color="black">'+str(row[5])+'</td>'
                    output+='<td><font size="3" color="blue">'+str(row[6])+'</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'GraduateScreen.html', context)

def ViewTeam(request):
    if request.method == 'GET':
        global uname
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Project ID</th><th><font size="3" color="black">Company Name</th>'
        output+='<th><font size="3" color="black">Application Type</th><th><font size="3" color="black">Project Description</th>'
        output+='<th><font size="3" color="black">Required Skills</th><th><font size="3" color="black">Project Posted Date</th>'
        output+='<th><font size="3" color="blue">Status</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM postproject where company_name='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="3" color="black">'+str(row[4])+'</td><td><font size="3" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="3" color="blue">'+str(row[6])+'</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'CompanyScreen.html', context) 

def getTeam(skills):
    teams = []
    a = skills.split(",")
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select applicant_name, email, skills FROM graduate_register")
        rows = cur.fetchall()
        for row in rows:
            name = row[0]
            email = row[1]
            applicant_skills = row[2]
            b = applicant_skills.split(",")
            matched = len(set(a).intersection(b)) / float(len(set(a)))
            print(str(a)+" === "+str(b)+" === "+str(matched))
            if matched > 0:
                teams.append([name, email, applicant_skills, matched])
    teams.sort(key = lambda x : x[3], reverse=True)
    return teams

def ApproveTeam(request):
    if request.method == 'GET':
        project_id = request.GET.get('id', False)
        members = request.GET.get('member', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update postproject set status='"+members+"' where project_id='"+project_id+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Members successfully assigned to project : "+project_id
        context= {'data': status}
        return render(request, 'AdminScreen.html', context)    

def ChooseTeam(request):
    if request.method == 'GET':
        project_id = request.GET.get('id', False)
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Project ID</th>'
        output+='<th><font size="3" color="blue">Team Member Name</th><th><font size="3" color="blue">Email ID</th>'
        output+='<th><font size="3" color="blue">Member Skills</th><th><font size="3" color="blue">Skills Percentage</th>'
        output+='</tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        skills = ""
        with con:    
            cur = con.cursor()
            cur.execute("select required_skills FROM postproject where project_id='"+project_id+"'")
            rows = cur.fetchall()
            for row in rows:
                skills = row[0]
                break            
        teams = getTeam(skills)
        members = ""
        for i in range(len(teams)):
            team = teams[i]
            if i == 0:
                output+='<tr><td><font size="3" color="black">'+project_id+'</td><td><font size="3" color="black">'+str(team[0])+' (Team Leader)</td><td><font size="3" color="black">'+str(team[1])+'</td>'
                output+='<td><font size="3" color="black">'+str(team[2])+'</td><td><font size="3" color="black">'+str(team[3])+'</td></tr>'                
                members += team[0]+", (Team Lead)"
            else:
                output+='<tr><td><font size="3" color="black">'+project_id+'</td><td><font size="3" color="black">'+str(team[0])+'</td><td><font size="3" color="black">'+str(team[1])+'</td>'
                output+='<td><font size="3" color="black">'+str(team[2])+'</td><td><font size="3" color="black">'+str(team[3])+'</td></tr>'
                members += team[0]+","
        if len(members) > 0:
            members = members[0:len(members)-1]
            output +='<tr><td><a href=\'ApproveTeam?id='+project_id+'&member='+members+'\'><font size=3 color=red>Click Here to Approved</font></a></td></tr>'        
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

def ApproveTeams(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Project ID</th><th><font size="3" color="black">Company Name</th>'
        output+='<th><font size="3" color="black">Application Type</th><th><font size="3" color="black">Project Description</th>'
        output+='<th><font size="3" color="black">Required Skills</th><th><font size="3" color="black">Project Posted Date</th>'
        output+='<th><font size="3" color="blue">Status</th>'
        output+='<th><font size="3" color="red">Click Here to Choose Teams</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM postproject where status='Pending'")
            rows = cur.fetchall()
            for row in rows:
                pid = row[0]
                cname = row[1]
                application_type = row[2]
                desc = row[3]
                skills = row[4]
                posted_date = row[5]
                status = row[6]
                output+='<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="3" color="black">'+str(row[4])+'</td><td><font size="3" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="3" color="black">'+str(row[6])+'</td>'
                output +='<td><a href=\'ChooseTeam?id='+str(row[0])+'\'><font size=3 color=blue>Choose Team</font></a></td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)  

def PostProjectAction(request):
    if request.method == 'POST':
        global uname
        application = request.POST.get('t1', False)
        description = request.POST.get('t2', False)
        skills = request.POST.getlist('t3')
        skills = ','.join(skills)
        dd = str(date.today())
        project_id = 0
        status = "error in posting job"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(project_id) FROM postproject")
            rows = cur.fetchall()
            for row in rows:
                project_id = row[0]
                break
        if project_id is not None:
            project_id += 1
        else:
            project_id = 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO postproject VALUES('"+str(project_id)+"','"+uname+"','"+application+"','"+description+"','"+skills+"','"+dd+"','Pending')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Project details successfully posted with project id = "+str(project_id)
        context= {'data': status}
        return render(request, 'CompanyScreen.html', context)

def PostProject(request):
    if request.method == 'GET':
       return render(request, 'PostProject.html', {})    

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def GraduateLogin(request):
    if request.method == 'GET':
       return render(request, 'GraduateLogin.html', {})

def CompanyLogin(request):
    if request.method == 'GET':
       return render(request, 'CompanyLogin.html', {})

def GraduateRegister(request):
    if request.method == 'GET':
       return render(request, 'GraduateRegister.html', {})    

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})   

def CompanyRegister(request):
    if request.method == 'GET':
       return render(request, 'CompanyRegister.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)

def GraduateLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select applicant_name, password FROM graduate_register where applicant_name='"+username+"' and password='"+password+"'")
            rows = cur.fetchall()
            for row in rows:
                uname = username
                index = 1
                break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'GraduateScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'GraduateLogin.html', context)        
    
def CompanyLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select company_name, password FROM company_register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'CompanyScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'CompanyLogin.html', context)

def Download(request):
    if request.method == 'GET':
        name = request.GET.get('file', False)
        with open("JobApp/static/resumes/"+name, "rb") as file:
            data = file.read()
        file.close()   
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response    

def ViewUsers(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Graduate Name</th><th><font size="3" color="black">Password</th>'
        output+='<th><font size="3" color="black">Contact No</th><th><font size="3" color="black">Email ID</th>'
        output+='<th><font size="3" color="black">Skills</th><th><font size="3" color="black">Resume File Name</th>'
        output+='<th><font size="3" color="blue">Download Resume</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from graduate_register")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="3" color="black">'+row[0]+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="3" color="black">'+row[2]+'</td><td><font size="3" color="black">'+row[3]+'</td>'
                output+='<td><font size="3" color="black">'+row[4]+'</td><td><font size="3" color="black">'+row[5]+'</td>'
                output +='<td><a href=\'Download?file='+row[5]+'\'><font size=3 color=blue>Download</font></a></td></tr>'
        output+= "</table></br>"

        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Company Name</th><th><font size="3" color="black">Password</th>'
        output+='<th><font size="3" color="black">Contact No</th><th><font size="3" color="black">Email ID</th>'
        output+='<th><font size="3" color="black">Skills</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from company_register")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="3" color="black">'+row[0]+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="3" color="black">'+row[2]+'</td><td><font size="3" color="black">'+row[3]+'</td>'
                output+='<td><font size="3" color="black">'+row[4]+'</td><td></tr>'
        output+= "</table></br></br></br></br>"   
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)    

def GraduateRegisterAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        skills = request.POST.getlist('t5')
        skills = ','.join(skills)
        myfile = request.FILES['t6'].read()
        fname = request.FILES['t6'].name
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select applicant_name FROM graduate_register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == name:
                    status = name+" applicant name already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO graduate_register VALUES('"+name+"','"+password+"','"+contact+"','"+email+"','"+skills+"','"+fname+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            if os.path.exists("JobApp/static/resumes/"+fname):
                os.remove("JobApp/static/resumes/"+fname)
            with open("JobApp/static/resumes/"+fname, "wb") as file:
                file.write(myfile)
            file.close()    
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup process successfully completed"
        else:
            status = "error in signup"        
        context= {'data': status}
        return render(request, 'GraduateRegister.html', context)

def CompanyRegisterAction(request):
    if request.method == 'POST':
        company = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        skills = request.POST.getlist('t5')
        skills = ','.join(skills)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select company_name FROM company_register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == company:
                    status = company+" name already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO company_register VALUES('"+company+"','"+password+"','"+contact+"','"+email+"','"+skills+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Company Signup process successfully completed"
        else:
            status = "error in signup"
        context= {'data': status}
        return render(request, 'CompanyRegister.html', context)


def EditProfile(request):
    if request.method == 'GET':
        global uname
        password = ""
        contact = ""
        email = ""
        skills = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select password, contact_no, email, skills FROM graduate_register where applicant_name='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                password = row[0]
                contact = row[1]
                email = row[2]
                skills = row[3]
                break
        output = '<tr><td><font size="3" color="black">Password</td><td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+password+'"></td></tr>'    
        output += '<tr><td><font size="3" color="black">Contact&nbsp;No</td><td><input type="text" name="t2" style="font-family: Comic Sans MS" size="15" value="'+contact+'"></td></tr>'    
        output += '<tr><td><font size="3" color="black">Email&nbsp;ID</td><td><input type="text" name="t3" style="font-family: Comic Sans MS" size="30" value="'+email+'"></td></tr>'
        context= {'data1': output}
        return render(request, 'EditProfile.html', context)             

def EditProfileAction(request):
    if request.method == 'POST':
        global uname
        password = request.POST.get('t1', False)
        contact = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        skills = request.POST.getlist('t4')
        skills = ','.join(skills)
        status = "error in editing profile"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'job',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update graduate_register set password='"+password+"', contact_no='"+contact+"', email='"+email+"', skills='"+skills+"' where applicant_name='"+uname+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        status = "Profile successfully updated"
        context= {'data': status}
        return render(request, 'GraduateScreen.html', context)    

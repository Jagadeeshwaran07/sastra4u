import math
import random
from smtplib import SMTP
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout


def index(request):

    if request.method == 'POST':

        CGPA = request.POST['CGPA']
        Credits = request.POST['Credits']
        Total_credits = request.POST['Total_credits']
        CGPA1=request.POST['CGPA1']
        Arrears=request.POST['Arrears']
      
        x=(float(CGPA1)*(int(Credits)+int(Total_credits))-float(CGPA)*int(Total_credits))/(int(Credits)+int(Arrears))

        if x>10:
           messages.info(request, 'Seems like your dream GPA is not possible this semester. Skills matters')
        else:
            messages.info(request,str(x) + " SGPA")
            return render(request, "sastra4u/index.html")

    return render(request, "sastra4u/index.html")

def attendance(request):
    if request.method == 'POST':

        credit = request.POST['credit']
        absent = request.POST['absent']

        bunk_remaining = (int(credit)*3) -1 - int(absent) 

        messages.info(request, "Can skip " + str(bunk_remaining) + ' more hours')
        return render(request, "sastra4u/index.html")
    return render(request, "sastra4u/index.html")

def queries(request):
    if request.method == 'POST':

        query = request.POST['query']
        email=request.POST['email']

        server = SMTP('smtp.gmail.com', 587) 
        server.starttls() 
        server.ehlo() 
        server.login("sastraforu@gmail.com","glevvsriasauxzux") 
        sent_from = "sastraforu@gmail.com" 
        to = "sastraforu@gmail.com"

        subject = 'Query from : ' + email

        message = 'Subject: {}\n\n{}'.format(subject, query)
        server.sendmail(sent_from, to, message) 
        messages.info(request, 'We received your query and will get back to your Mail within 24 hours!')
        return render(request,"sastra4u/index.html")

    return render(request,"sastra4u/index.html")

def gradecalculation(request):

    if request.method == "POST":
        x = request.POST['internal']
        
        for i in range(101):
            if int(x) + i == 91:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'S grade: ' +  str(g))

        for i in range(101):
            if int(x) + i == 86:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'A+ grade: ' +  str(g))

        for i in range(101):
            if int(x) + i == 75:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'A grade: ' +  str(g))

        for i in range(101):
            if int(x) + i == 66:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'B grade: ' +  str(g))

        for i in range(101):
            if int(x) + i == 55:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'C grade: ' +  str(g))

        for i in range(101):
            if int(x) + i == 50:
                if i*2 <= 100:
                    g = i*2
                    messages.info(request, 'D grade: ' +  str(g))
                    

        return render(request, "sastra4u/index.html")
     
    return render(request,"/")

def register(request):

    if request.method == "POST":
         
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        email = request.POST['email']
        course = request.POST['course']
        # sem = request.POST['sem']

        if pass1 == pass2:

            if User.objects.filter (username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Already account created')
                return redirect('register')
            else:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name = course
                # myuser.last_name = sem        

                myuser.save()

                digits = "0123456789"
                OTP = ""

                for i in range(4):
                    OTP+=digits[math.floor(random.random()*10)]

                otp1 = OTP + " is your Verification OTP"
                msg = otp1

                request.session['OTP'] = OTP

                server = SMTP('smtp.gmail.com', 587) 
                server.starttls() 
                server.ehlo() 
                server.login("sastraforu@gmail.com","glevvsriasauxzux") 
                sent_from = "sastraforu@gmail.com" 
                to = email

                subject = 'sastra4u OTP Verification'

                message = 'Subject: {}\n\n{}'.format(subject, msg)
                server.sendmail(sent_from, to, message) 
                messages.info(request, 'Verification OTP sent to email')
                return redirect('register')
            
        else:
           messages.info(request, 'Password Not Matching') 
           return redirect('register')

    return render(request, "sastra4u/register.html")

def check_otp(request):
    
    if request.method == 'POST': 
        otp = request.POST['otp']

        if otp == request.session['OTP']:
            messages.success(request, 'Your Account has been successfully created.')
            return render(request,"sastra4u/signin.html")
        
        else:
            messages.info(request, 'OTP mismatch, Kindly Check and submit again')  
            return redirect('register')
     
    return redirect('register')

def signin(request):

    if request.method == 'POST':

        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, 'sastra4u/index.html')
        
        else:
            messages.error(request, "Bad Credentials")
            return render(request, "sastra4u/signin.html")

    return render(request, "sastra4u/signin.html")

def YourSyllabus(request):

    if request.method == 'POST':
      course = request.POST['syllabus']

    if course == "Aerospace Engineering":
        return redirect("https://www.sastra.edu/prog/SoME/BAS/")
    if course == "Bioengineering":
        return redirect("https://www.sastra.edu/prog/SCBT/BBE/")
    if course == "Bioinformatics":
        return redirect("https://www.sastra.edu/prog/SCBT/BBI/")
    if course == "Biotechnology":
        return redirect("https://www.sastra.edu/prog/SCBT/BBT/")
    if course == "Chemical Engineering":
        return redirect("https://www.sastra.edu/prog/SCBT/BCH/")
    if course == "Civil Engineering":
        return redirect("https://www.sastra.edu/prog/SoCE/BCE/")
    if course == "Computer Science & Business Systems":
        return redirect("https://www.sastra.edu/prog/SoC/BCSBS/")
    if course == "Computer Science & Engineering":
        return redirect("https://www.sastra.edu/prog/SoC/BCS/")
    if course == "Computer Science & Engineering (Artificial Intelligence & Data Science)":
        return redirect("https://www.sastra.edu/prog/SoC/BCSAID/")
    if course == "Comptuer Science & Engineering (Cyber Security & Block Chain Technology)":
        return redirect("https://www.sastra.edu/prog/SoC/BCSCBT/")
    if course =="Computer Science & Engineering (IoT & Automation)</option>":
        return redirect("https://www.sastra.edu/prog/SoC/BCSIA/")
    if course =="Electrical and Electronics Engineering":
        return redirect("https://www.sastra.edu/prog/SEEE/BEE/")
    if course =="Electrical and Electronics Engineering (Smart Grid and Electric Vehicles)":
        return redirect("https://www.sastra.edu/prog/SEEE/BEESGV/")
    if course =="Electronics & Communication Engineering":
        return redirect("https://www.sastra.edu/prog/SEEE/BEC/")
    if course =="Electronics & Communication Engineering (CPS)":
        return redirect("https://www.sastra.edu/prog/SEEE/BECCPS/")
    if course =="Electronics & Instrumentation Engineering":
        return redirect("https://www.sastra.edu/prog/SEEE/BEI/")
    if course =="Robotics & Artificial Intelligence":
        return redirect("https://www.sastra.edu/prog/SEEE/BRAI/")
    if course =="Electronics Engineering (VLSI Design & Technology":
        return redirect("https://www.sastra.edu/prog/SEEE/BEEVDT/")
    if course =="Information and Communcation Technology":
        return redirect("https://www.sastra.edu/prog/SoC/BIC/")
    if course =="Information Technology":
        return redirect("https://www.sastra.edu/prog/SoC/BIT/")
    if course =="Mechanical Engineering":
        return redirect("https://www.sastra.edu/prog/SoME/BME/")
    if course =="Mechanical Engineering (Digital Manufacturing)":
        return redirect("https://www.sastra.edu/prog/SoME/BMEDM/")
    if course =="Mechatronics":
        return redirect("https://www.sastra.edu/prog/SoME/BMT/")


    return render(request,"sastra4u/index.html")

def signout(request):
    logout(request)
    return redirect('signin')
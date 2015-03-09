from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
import hashlib
import datetime
from login.models import *
import re

def studentComplainView(request):
	uid=request.session.get('uid')
	ComplainObjects = Complain.objects.all().filter(uid = uid)
	return render_to_response('student/viewStudComplain.html',{'list' : ComplainObjects});

	
def studentLodgeComplain(request):
	return render_to_response('student/studLodgeComplain.html');

def studentHome(request):
	return render_to_response('student/studentHome.html');

def studentProfile(request):
	return render_to_response('student/studentProfile.html');

def studentViewRate(request):
	return render_to_response('student/studViewRate.html');

def studentPoll(request):
	return render_to_response('student/studPoll.html');

def studentHostelLeave(request):
	return render_to_response('student/studHostelLeave.html');

def studentMessRebate(request):
	return render_to_response('student/messrebate.html');

def getCatagory(str):
	if str == "Mess":
		return 1
	elif str == "Environment":
		return 2
	elif str == "Technical":
		return 3
	elif str == "Maintenance":
		return 4
	else:
		return 0

def getTypeDescription(code):
	if code == 1:
		return "Mess"
	elif code == 2:
		return "Environment"
	elif code == 3:
		return "Technical"
	elif code == 4:
		return "Maintenance"
	else:
		return "Other"


def lodgeComplainDetail(request):
	subject=request.POST.get('subject');
	detail=request.POST.get('message');
	catagory=getCatagory(request.POST.get('catagory'));
	hostel=request.session.get("hostel");
	time=datetime.datetime.now();
	uid=request.session.get('uid');	
	history = "Complain added by " + request.session.get("name") + " at time : " + str(time) 
	complainObj=Complain(uid = uid , time = time , hostel = hostel, type=catagory , subject	= subject, detail = detail, comments = 0, history = history );
	complainObj.save();
	secretaryObj = Secretary.objects.get(hostel=hostel, type=catagory)
	secid = secretaryObj.uid
	cid=(Complain.objects.get(uid = uid , time = time)).cid
	CLObj = Complainlink(cid = cid, studid = uid, secid = secid)
	CLObj.save()
	return redirect('../complainView/');

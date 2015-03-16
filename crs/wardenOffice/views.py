from django.shortcuts import render
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
from student.views import getTypeDescription,getCatagory

def isWardenOffice(request):
	user_type = request.session.get("user_type",'')
	if user_type != "wardenOffice":
		return False
	else:
		return True

def wardenOfficeComplainView(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	# PublicComplainObjects = Complainlink.objects.all?().filter(wardenid = uid).filter(studid = 0);
	query1 = 'SELECT * FROM complainLink WHERE woID = ' + str(uid) + ' AND studID = 0'
	PublicComplainObjects = Complainlink.objects.raw(query1)
	query2 = 'SELECT * FROM complainLink WHERE woID = ' + str(uid) + ' AND studID != 0'
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	# PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Privatelist=[];
	Publiclist=[];
	for num in PrivateComplainObjects:
		numCid=num.cid
		Privatelist.append(Complain.objects.get(cid=numCid));		#username  in fac table
	for num in PublicComplainObjects:
		numCid=num.cid
		Publiclist.append(Complain.objects.get(cid=numCid));
	return render_to_response('wardenOffice/wardenAllComplain.html',{'list1' : Publiclist, 'list2':Privatelist});

def wardenOfficeHome(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	return render_to_response('wardenOffice/wardenHome.html', {'msg' : request.session.get('name') });

def forwardToWardenOffice(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	complainArray=request.POST.getlist('complain')
	length = len(complainArray)
	for x in range(0,length):
		comid = complainArray[x]
		ClO =Complainlink.objects.get(cid=comid)
		hostel=(Complain.objects.get(cid=comid)).hostel
		wardenId = (Warden.objects.get(hostel=hostel)).fid
		ClO.wardenid = wardenId
		ClO.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('../wardenComplain');


def viewSecretary(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	# try:
	uid=request.session.get('uid')
	ashokaseclist=[];
	aryabhattaseclist=[];
	chanakya1seclist=[];
	chanakya2seclist=[];
	test=[1,2,3,4];
	for num in test:
		ashokaseclist.append(Secretary.objects.filter(hostel = 0).filter(type = num));
		aryabhattaseclist.append(Secretary.objects.filter(hostel = 1).filter(type = num));
		chanakya1seclist.append(Secretary.objects.filter(hostel = 2).filter(type = num));
		chanakya2seclist.append(Secretary.objects.filter(hostel = 3).filter(type = num));
	return render_to_response('wardenOffice/wardenOfficeViewComplain.html',{'list1':ashokaseclist, 'list2' :aryabhattaseclist,'list3':chanakya1seclist,'list4':chanakya2seclist});
	# except:
	# 	return render_to_response('login/loginPage.html');

# def ForwardComplain(request):
	# try:
		# uid=request.session.get('uid');
		# 
	# except:
		# return render_to_response('login/loginPage.html');



# Create your views here.


# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# from datetime import datetime, timedelta
import datetime as dt
# Create your views here.

from servicemonitor.models import SmMstservice, SmTrnregister, SmImpact, SmMstmonitorwindow

def home(request):
    minorcategory = ['Virtual Server','Server','Device','Service','Storage','Firewall','Virtual Host server','Switches, cables','Facility']
    now = dt.datetime.now()
    year = now.year
    month = now.month
    days = calendar.monthrange(now.year, now.month)[1]
    cal = calendar.Calendar()
    sundays = []
    saturdays = []
    for day in cal.itermonthdates(year, month):
        if day.weekday() == 6 and day.month == month:
            sundays.append(day)
        if day.weekday() == 5 and day.month == month:
            saturdays.append(day)
    weekoff = len(sundays)
    satoff = len(saturdays)
    expectuptime = (24*60*(days-weekoff-3)-(satoff*16*60))
    return render(request, 'servicemonitor/home.html', context={'expectuptime':expectuptime, 'minorcategory':minorcategory})

def breakdown(request):
    return render(request, 'servicemonitor/breakdown.html')

def service(request):
    servicequeryset = SmMstservice.objects.filter(category="S").order_by('status', 'importance')
    serviceList = []
    for service in servicequeryset:
        from django.db.models import Sum
        downtime = 0
        downtime = SmTrnregister.objects.filter(esid = service.esid).aggregate(Sum ('downtime'))
        if downtime.get('downtime__sum') != None:
            downtime = downtime.get('downtime__sum')
        else:
            downtime = 0
        serviceList.append({'status':service.status, 'esid':service.esid,'esname':service.esname,
                            'minorcategory':service.minorcategory,'importance':service.importance,
                            'expectuptime':service.expectuptime,'plandowntime': downtime})

    data = {'data': list(serviceList)}
    return JsonResponse(data, safe=False)

def equipment(request):

    EquipList = SmMstservice.objects.filter(category="E").order_by('status', 'importance')

    EquipmentList = []
    for equipment in  EquipList:
        from django.db.models import Sum
        downtime = 0
        downtime = SmTrnregister.objects.filter(esid=equipment.esid).aggregate(Sum('downtime'))
        if downtime.get('downtime__sum') != None:
            downtime = downtime.get('downtime__sum')
        else:
            downtime = 0
        EquipmentList.append({'status': equipment.status, 'esid': equipment.esid, 'esname': equipment.esname,
                            'minorcategory': equipment.minorcategory, 'importance': equipment.importance,
                            'expectuptime': equipment.expectuptime, 'plandowntime': downtime})

    data = {'data': list(EquipmentList)}
    return JsonResponse(data, safe=False)

def service_monitor(request):
    se_List = SmMstservice.objects.all().values('status', 'esid', 'shortname', 'esname', 'category', 'minorcategory', 'importance', 'units', 'mis', 'expectuptime', 'plandowntime', 'acceptuptime').order_by('status', 'importance')
    data = {'data': list(se_List)}
    return JsonResponse(data, safe=False)

def stop(request, pk):
    serviceList = SmMstservice.objects.get(esid=pk)
    if request.method == 'POST':
        print "Inside POST Method"*4
    return render(request, "servicemonitor/stop.html",context={ 'serviceList': serviceList})


def start(request, pk):
    serviceList = SmMstservice.objects.get(esid=pk)
    smtrnregister=SmTrnregister.objects.filter(esid=pk).last()
    from django.utils import timezone
    enddate = timezone.now()
    total_time = enddate - smtrnregister.startdate
    impact_val = total_time.total_seconds()
    return render(request, "servicemonitor/start.html", context={'serviceList': serviceList,"SmTrnregister":smtrnregister, 'total_time':total_time, 'impact_val':impact_val})


def register(request):
    registerlist = SmTrnregister.objects.all()
    startdate = SmTrnregister.objects.values_list('startdate')
    return render(request, 'servicemonitor/register.html')


def uptimeregister(request):
    registerlist = SmTrnregister.objects.all().values('entryid','startdate','entryby','esid','category','importance','description','downtypetime','source','impact','enddate','downtime','closemailsent','closeby','rc','ca','mis').order_by('-entryid')
    data = {'data': list(registerlist)}
    return JsonResponse(data, safe=False)


def add(request):
    if request.method == "POST":
        esid = request.POST['inputesid']
        shortname = request.POST['inputshortname']
        esname = request.POST['inputesname']
        category = request.POST['inputcategory']
        minorcategory = request.POST['inputminor']
        importance = request.POST['inputimportance']
        units = request.POST['inputunits']
        mis = request.POST['inputmis']
        plandowntime = request.POST['inputplandowntime']
        expectuptime = request.POST['inputexpectuptime']
        acceptuptime = request.POST['inputacceptuptime']
        newservice = SmMstservice(esid=esid, shortname=shortname, esname=esname,
                             category=category,
                             minorcategory=minorcategory, importance=importance, units=units,
                           mis=mis, plandowntime=plandowntime, expectuptime=expectuptime, acceptuptime=acceptuptime)

        newservice.save()
    return HttpResponseRedirect(reverse('home'))

def stopped(request,pk):
 if request.method == "POST":
     serviceList = SmMstservice.objects.get(esid=pk)
     serviceList.status = False
     serviceList.save()
     data=request.POST.copy()
     mis = request.POST['mis']
     SmTrnregister.objects.create(esid=serviceList,startdate=datetime.datetime.today(),source=data['source'],closemailsent=1,downtypetime=data['downtypetime'],mis=data['mis'],description=data['description'],importance=data['importance'],category=data['category'])
 return HttpResponseRedirect(reverse('home'))
     # return render(request, "servicemonitor/stop.html", context={'serviceList': serviceList})

def started(request,pk):
    if request.method == "POST":
        data = request.POST.copy()
        serviceList = SmTrnregister.objects.filter(esid=pk).last()
        # downtime = dt.datetime.strptime(data['downtime'], '%H:%M:%S')
        downtime = str(data['downtime']).split('.')[0]
        downtime = sum(x * int(t) for x, t in zip([3600, 60, 1], downtime.split(":")))
        print "********END DATE TIME&&&&&&&&&&&",dt.datetime.now()
        serviceList.enddate = dt.datetime.now()
        serviceList.rc = data['rc']
        serviceList.ca = data['ca']
        serviceList.impact = data['impact']
        serviceList.downtime = downtime
        serviceList.save()
        serviceLists = SmMstservice.objects.get(esid=serviceList.esid.esid)
        serviceLists.status = 1
        serviceLists.save()

    return HttpResponseRedirect(reverse('home'))

def breakdownall(request):
    serviceLists = SmMstservice.objects.get(status=1)
    serviceLists.status = 0
    serviceLists.save()
    return HttpResponseRedirect(reverse('home'))
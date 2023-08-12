from django.shortcuts import render, redirect, resolve_url
from .models import Client, Personnel
# Create your views here.
from django.http import HttpResponse
from .connection import collectionsFromMongo as cfm
from django.utils.timezone import now


def home(request):
    return render(request, 'home.html', {})


def client(request):
    clients = Client.objects.all()
    return render(request, 'home.html', {'clients': clients, 'length': len(clients)})


def personnel(request):
    personnel = Personnel.objects.all()
    return render(request, 'home.html', {'personnel': personnel})


def get_client(request, pk):
    if request.user.is_authenticated:
        client = Client.objects.filter(clientCode=pk)
        if len(client) != 0:
            personnel = Personnel.objects.all()
            return render(request, 'home.html', {'clients': client, 'assigned': personnel})
        else:
            return MessageRedirect('The client doesn\'t exist.', 'client')
    else:
        return redirect('home')


def add_client(request):
    if request.user.is_authenticated:
        zero = Personnel(firstname='-', id=0, lastname='-',
                         personnelID=0, username='_._')
        personnel = Personnel.objects.all()
        personnel = list(personnel)
        personnel.insert(0, zero)
        return render(request, 'addClient.html', {'personnel': personnel})
    else:
        return redirect('home')


def added_client(request):
    if request.user.is_authenticated:
        collection = cfm('crm_app_client')
        lastEntryCol = cfm('last_entry')
        personnelCol = cfm('crm_app_personnel')
        lastEntry = lastEntryCol.find_one()
        newClient = {'clientCode': lastEntry['clientCode']+1}
        newClient['id'] = newClient['clientCode']
        if request.method == "POST":
            newClient['company'] = request.POST["Name"]
            newClient['dateCreated'] = now()
            newClient['address'] = request.POST["Address"]
            newClient['personnelID'] = int(request.POST["Assigned"])
        if newClient['company'] == '':
            return MessageRedirect('No Company Name Given.', 'add_client')
        if newClient['personnelID'] == 0:
            return MessageRedirect('No Personnel Selected. Please select an assigned personnel.', 'add_client')
        else:
            assigned = personnelCol.find_one(
                {'personnelID': int(newClient['personnelID'])})
            newClient['assigned_personnel'] = assigned['firstname'] + \
                ' '+assigned['lastname']
        try:
            collection.insert_one(newClient)
            lastEntryCol.update_one({'clientCode': lastEntry['clientCode']}, {
                                    "$set": {'clientCode': newClient['clientCode']}})
        except Exception as e:
            MessageRedirect(e, 'add_client')

        return render(request, 'added.html', {'newClient': newClient})
    else:
        return redirect('home')


def edit(request):
    if request.user.is_authenticated:
        clientCol = cfm('crm_app_client')
        update = {}
        if request.method == "POST":
            current = clientCol.find_one(
                {'clientCode': int(request.POST['clientCode'])})
            for i in ['company', 'address', 'personnelID']:
                if str(current[i]) != str(request.POST[i]):
                    if i == 'personnelID':
                        update[i] = int(request.POST[i])
                        personneldb = cfm('crm_app_personnel')
                        personneldb = personneldb.find_one(
                            {'personnelID': update[i]})
                        update['assigned_personnel'] = personneldb['firstname'] + \
                            ' '+personneldb['lastname']
                    else:
                        update[i] = str(request.POST[i])
            clientCol.update_one(
                {'clientCode': int(request.POST['clientCode'])}, {"$set": update})
        return MessageRedirect('Client Updated', 'get_client', int(request.POST['clientCode']))
    else:
        return redirect('home')


def delete(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            clientCol = cfm('crm_app_client')
            if request.method == "POST":
                try:
                    clientCol.delete_one(
                        {'clientCode': int(request.POST['clientCode'])})
                except Exception as e:
                    MessageRedirect(e, 'client')
            return MessageRedirect('Client with code %s deleted' % request.POST['clientCode'], 'client')
        else:
            return MessageRedirect('You are not authorized to delete this client', 'client')
    else:
        return redirect('home')


def MessageRedirect(message, redirectPage, args=None):
    if args is not None:
        resolved = resolve_url(redirectPage, args)
    else:
        resolved = resolve_url(redirectPage)
    redirection = '<script>'
    redirection += 'var start = new Date().getTime() + 5000;'
    redirection += 'setTimeout(\"location.href = \'' + \
        resolved + '\';\",5000);'
    redirection += 'var x = setInterval(function() {'
    redirection += 'var interval = Math.floor((start - new Date().getTime())/1000);'
    redirection += 'document.getElementById("seconds").innerHTML = interval;'
    redirection += 'if(interval<0){'
    redirection += 'clearInterval(x);'
    redirection += 'document.getElementById("seconds").innerHTML = 0;}'
    redirection += '}, 1000);'
    redirection += '</script>'
    return HttpResponse('<div>' + message + ' Redirecting you to ' + redirectPage + ' page in <span id="seconds">__</span> seconds.</div>' + redirection)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from _datetime import datetime

from django.db.models import Max


def index(request):
    return render(request, 'index.html')


def login(request):
    request.session['account'] = False
    if request.method == 'POST':
        username = request.POST.get('UserName')
        password = request.POST.get('password')
        if Login.objects.filter(username=username, password=password).exists():
            request.session['account'] = True
            request.session['username'] = username
        if request.session['account']:
            return redirect('loginsuccess')

        else:
            messages.success(request, "Username and Password do not match.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('UserName')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        accounttype = request.POST.get('role')
        username = username.lower()
        username.replace(" ", "")
        email = email.lower()
        email.replace(" ", "")
        data = Register(Full_Name=fullname, username=username, Email=email, password=password,
                        contact=contact, Gender=gender, Account_type=accounttype)
        data1 = Login(username=username, password=password)
        try:
            data.full_clean()
            data1.full_clean()
            data.save()
            data1.save()
            messages.success(request, 'Registeration Completed')
            return redirect('index')
        except:
            html = "<html><body> ERROR</body></html>"
            return HttpResponse(html)

    return render(request, 'signup.html')


def loginsuccess(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        logos = Logo_listing.objects.filter(Status='1')
        n = len(logos)
        params = {'u_id': u_id, 'logos': logos, 'range': range(0, n)}
        return render(request, 'loginsuccess.html', params)
    return redirect('login')


def mylogo(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        if Logo_listing.objects.filter(Owner=u_id).exists():
            album = Logo_listing.objects.filter(Owner=u_id)
            n = len(album)
            params = {'u_id': u_id, 'album': album, 'range': range(0, n), 'n': n}
            if 'auction' in request.POST:
                u_title = request.POST.get('auction')
                request.session['u_title'] = u_title
                return redirect('BidUpload')
            return render(request, 'designer.html', params)
        else:
            n = 0
            params = {'n': n}
            return render(request, 'designer.html', params)
    return redirect('login')


def BidUpload(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        u_title = request.session['u_title']
        params = {'u_title': u_title}
        if request.method == 'POST':
            start_price = request.POST.get('startprice')
            start_date = request.POST.get('start')
            end_date = request.POST.get('end')
            data = Logo_Bid_details(Title=u_title, AuctionStart=start_date, AuctionEnd=end_date,
                                    StartBidAmount=start_price)
            info = Bids(Title=u_title, Bidder=u_id, Amount=start_price)
            try:
                data.full_clean()
                data.save()
                info.save()
                Logo_listing.objects.filter(Title=u_title).update(Status='1')
                del request.session['u_title']
                messages.success(request, 'Logo Auctioned successful')
                return redirect('mylogo')
            except:
                del request.session['u_title']
                messages.error(request, 'Already Auctioned')
        return render(request, 'bid_form.html', params)


def upload(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        if request.method == 'POST':
            title = request.POST.get('logoname')
            description = request.POST.get('desc')
            image = request.FILES.get('file')
            data = Logo_listing(Title=title, Description=description, Image=image, Creator=u_id, Owner=u_id)
            try:
                data.full_clean()
                data.save()
                html = "<html><body> Logo Uploaded</body></html>"
                return HttpResponse(html)
            except:
                print("Error")
        return render(request, 'upload.html')

    return redirect('login')


def view(request):
    check = request.session['account']
    if check:
        title = request.POST.get('view')
        data = Logo_listing.objects.get(Title=title)
        data1 = Logo_Bid_details.objects.get(Title=title)
        data2 = Bids.objects.filter(Title=title)
        current = data2.aggregate(Max('Amount'))['Amount__max']
        new_current_owner = Bids.objects.get(Title=title, Amount=current).Bidder
        owner = data.Owner
        desc = data.Description
        img = data.Image
        base = data1.StartBidAmount
        end = data1.AuctionEnd
        diff = countdown(end)
        if diff.total_seconds() <= 0:
            Logo_listing.objects.filter(Title=title).update(Status='0')
            Logo_listing.objects.filter(Title=title).update(Owner=new_current_owner)
            Logo_Bid_details.objects.get(Title=title).delete()
            Bids.objects.filter(Title=title).delete()
            return redirect('loginsuccess')
        params = {'title': title, 'owner': owner, 'desc': desc, 'img': img, 'base': base, 'current': current, 'end': end
                  , 'diff': diff}

        return render(request, 'logoview.html', params)
    return redirect('login')


def countdown(end):
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    end = end.strftime("%Y-%m-%d %H:%M:%S")
    d1 = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    diff = d2 - d1
    return diff


def bid_increase(request):
    check = request.session['account']
    if check:
        title = request.POST.get('bid')
        u_id = request.session['username']
        data2 = Bids.objects.filter(Title=title)
        current = data2.aggregate(Max('Amount'))['Amount__max']
        value = current + 100
        if Bids.objects.filter(Title=title, Bidder=u_id).exists():
            Bids.objects.filter(Title=title, Bidder=u_id).update(Amount=value)
        else:
            info = Bids(Title=title, Bidder=u_id, Amount=value)
            info.save()
        messages.success(request, '+100 Bidded for ' + title)
        return redirect('loginsuccess')


def edit_profile(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        data = Register.objects.filter(username=u_id)
        n = len(data)
        if request.method == 'POST':
            Full_Name = request.POST.get('name')
            Contact = request.POST.get('contact')
            Register.objects.filter(username=u_id).update(Full_Name=Full_Name, contact=Contact)
            return redirect('edit_profile')
        params = {'u_id': u_id, 'data': data, 'range': range(0, n)}
        return render(request, 'profile.html', params)


def mybids(request):
    check = request.session['account']
    if check:
        u_id = request.session['username']
        Bids.objects.(Bidder=u_id)
        title = Bids.Title
        if Logo_Bid_details.objects.filter(Title=title).exists():
            bids = Bids.objects.filter(Bidder=u_id)
            return render(request, 'mybids.html', {'bids': bids})
        else:
            return render(request, 'mybids.html')



def logout(request):
    try:
        request.session['account'] = False
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')

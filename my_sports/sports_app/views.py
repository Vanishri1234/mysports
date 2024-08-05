import datetime
import json
import random
from urllib import request

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.checks import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .forms import EnquiryForm
from .models import Enquiry, AddRegister, Duration, coachReg, Coach_allocation, KitItem, Item_entry, kit_distribution


# Create your views here.

def admin(request):
    return render(request,"admin.html")


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('home')  # Replace 'dashboard' with your actual URL name
        else:
            # Handle invalid login
            return render(request, 'admin.html', {'error_message': 'Invalid username or password.'})

    # If it's not a POST request, render the initial form or page
    return render(request, 'home.html')




#Enquiry
def enquiry_form(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        date_of_birth = request.POST.get('dateOfBirth')
        gender = request.POST.get('gender')
        contact_no = request.POST.get('contactNo')
        parent_name = request.POST.get('parentName')
        parent_mobile_no = request.POST.get('parentMobileNo')
        parent_email = request.POST.get('parentEmail')
        parent_address = request.POST.get('parentAddress')
        weekly_sessions = request.POST.get('weeklySessions')
        how_did_you_know = request.POST.get('howDidYouKnow')
        other_details = request.POST.get('otherDetails')
        age = request.POST.get('age')


        # Calculate age based on date of birth


        # Save the data to the database (assuming you have a model named Enquiry)
        enquiry = Enquiry(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_no=contact_no,
            parent_name=parent_name,
            parent_mobile_no=parent_mobile_no,
            parent_email=parent_email,
            parent_address=parent_address,
            weekly_sessions=weekly_sessions,
            how_did_you_know=how_did_you_know,
            other_details=other_details,
            age=age,

        )
        enquiry.save()

        # Redirect after successful form submission (optional)
        return redirect('enquiry_list')

    # Render the form template if it's a GET request
    return render(request, 'Enquiry/players_enquiry.html')

def player_list(request):
    enquiries=Enquiry.objects.all()
    return render(request,'Enquiry/player_list.html',{'enquiries':enquiries})


def enquiry_list(request):
    player_name = request.GET.get('q')
    age = request.GET.get('age')
    mobile_number = request.GET.get('mobile')

    # Initial queryset
    data = Enquiry.objects.all()

    # Apply filters if they exist
    if player_name:
        data = data.filter(first_name__icontains=player_name)
    if age:
        data = data.filter(age=age)
    if mobile_number:
        data = data.filter(contact_no__icontains=mobile_number)

    return render(request, 'Enquiry/enquiry_list.html', {'data': data})

def edit_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        form = EnquiryForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            return redirect('enquiry_list')  # Redirect to the list view
    else:
        form = EnquiryForm(instance=enquiry)

    context = {'form': form}
    return render(request, 'Enquiry/edit_enquiry.html', context)


def delete_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        return redirect('enquiry_list')  # Redirect to the list view

    return render(request, 'confirm_delete.html', {'enquiry': enquiry})




def register(request):
    if request.method == "POST":

        now = datetime.datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        admission_no = random.randint(1111, 9999)
        adm_no = str(admission_no)

        invoice_ID = random.randint(1111, 9999)
        invoice = str(invoice_ID)


        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        adhar = request.POST.get('adhar')
        parentName = request.POST.get('parentName')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        place = request.POST.get('place')
        address = request.POST.get('address')
        uniformSize=request.POST.get('uniformSize')
        uniformColor=request.POST.get('uniformColor')
        package=request.POST.get('package')
        sessions=request.POST.get('sessions')
        totalAmount=request.POST.get('totalAmount')
        blood_group=request.POST.get('blood_group')
        payment=request.POST.get('payment')
        balance=request.POST.get('balance')
        batchtime=request.POST.get('batchtime')
        name=request.POST.get('name')




        AddRegister.objects.create(admission_no=adm_no,
                                date=con_date,
                                dob=dob,
                                gender=gender,
                                phone=phone,
                                adhar=adhar,
                                parentName = parentName,
                                mobile= mobile,
                                email=email,
                                place=place,
                                address=address,
                                uniformSize=uniformSize,
                                uniformColor=uniformColor,
                                package=package,
                                sessions=sessions,
                                totalAmount=totalAmount,
                                invoice_ID = invoice,
                                blood_group=blood_group,
                                payment=payment,
                                balance=balance,
                                batchtime=batchtime,
                                name=name

        )
        return redirect('receipt',admission_no=adm_no)
    return render(request,'Admission/admission.html')

def fetch_coach_type(request):
    if request.method == 'POST':
        coach_name = request.POST.get('coachname')
        try:
            coach = coachReg.objects.get(coachname=coach_name)
            return JsonResponse({'coachType': coach.coachtype})
        except coachReg.DoesNotExist:
            return JsonResponse({'coachType': ''})
    return JsonResponse({'coachType': ''})

def get_coach_type(request, coach_id):
    try:
        coach = coachReg.objects.get(id=coach_id)
        return JsonResponse({'coachType': coach.coachType})
    except coachReg.DoesNotExist:
        return JsonResponse({'error': 'Coach not found'}, status=404)


def receipt(request,admission_no):
    admission=get_object_or_404(AddRegister,admission_no=admission_no)
    return render(request,'Admission/Recipt.html',{'admission':admission})



def register_form(request,admission_no):
    admission=get_object_or_404(AddRegister,admission_no=admission_no)
    return render(request,'Admission/admission_form.html',{'admission':admission})

def admission_list(request):
    mobile = request.GET.get('mobile', '')
    admission_no = request.GET.get('admission_no', '')

    admissions = AddRegister.objects.all()

    if mobile:
        admissions = admissions.filter(mobile__icontains=mobile)

    if admission_no:
        admissions = admissions.filter(admission_no__icontains=admission_no)

    context = {
        'data': admissions,
    }
    return render(request, 'Admission/admission_list.html', context)

def edit_admission(request, pk):
    admission = get_object_or_404(AddRegister, id=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=admission)
        if form.is_valid():
            form.save()
            return redirect('admission_list')
    else:
        form = RegisterForm(instance=admission)
    return render(request, 'Admission/edit_admission.html', {'form': form})

def delete_admission(request, pk):
    admission = get_object_or_404(AddRegister, id=pk)
    if request.method == 'POST':
        admission.delete()
        return redirect('admission_list')
    return render(request, 'admission_list.html', {'data': AddRegister.objects.all()})
def home(request):
    return render(request,"home.html")


def sessions(request):
    if request.method=="POST":
        session=request.POST.get('session')
        weekly=request.POST.get('weeklySessions')
        pay=request.POST.get('amount')

        Duration.objects.create(
            session=session,
            weekly_sessions=weekly,
            amount=pay
        )
        return redirect('sessions')
    return render(request,'Admission/sessions.html')

def duration(request):
    duration = Duration.objects.all()
    return render(request, 'Admission/admission.html', {'duration': duration})


def coach_reg(request):
    if request.method == 'POST':
        # Extract data from the form
        coachname = request.POST.get('coachname')
        adhar=request.POST.get('adhar')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        coachType = request.POST.get('coachType')
        address=request.POST.get('address')
        document=request.POST.get('document')

        coachReg.objects.create(
            coachname=coachname,
            email=email,
            phone=phone,
            coachType=coachType,
            adhar=adhar,
            address=address,
            document=document

        )
        return redirect('coach_reg')
    return render(request, 'coaches/coach_Reg.html')




def player_name(request):
    rName = AddRegister.objects.all()
    cName = coachReg.objects.all()
    return render(request, 'coaches/coach_allocation.html', {'rName': rName, 'cName': cName})


def coach_allocation(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        session = request.POST.get('session')
        batchtime = request.POST.get('batchtime')
        coachname = request.POST.get('coachname')
        coachType = request.POST.get('coachType')


        Coach_allocation.objects.create(
            first_name=first_name,
            last_name=last_name,
            session=session,
            batchtime=batchtime,
            coachname=coachname,
            coachType=coachType

        )

        return redirect('coach_allocation')
    return render(request, 'coaches/coach_allocation.html')


def fetch_name_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            player = get_object_or_404(AddRegister, name=name)
            data = {

                'session': player.sessions,
                'batchtime':player.batchtime
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid  name'})
    return JsonResponse({'error': 'Invalid request method'})

def fetch_coach_data(request):
    if request.method == 'POST':
        coachname = request.POST.get('coachname')
        if coachname:
            coach = get_object_or_404(coachReg, coachname=coachname)
            data = {
                'coachType': coach.coachType,

            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid coach name'})
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def kit_entry(request):
    if request.method == "POST":
        brand_names = request.POST.getlist('brand_name[]')
        no_of_stocks = request.POST.getlist('no_of_stock[]')
        unit_prices = request.POST.getlist('unit_price[]')

        for brand_name, no_of_stock, unit_price in zip(brand_names, no_of_stocks, unit_prices):
            KitItem.objects.create(
                brand_name=brand_name,
                no_of_stock=no_of_stock,
                unit_price=unit_price
            )

        return redirect('kit_entry')

    return render(request, 'stock/kit_entry.html')

def kit_list(request):
    kits = KitItem.objects.all()
    return render(request, 'stock/kit_list.html', {'kits': kits})

def edit_kit(request, kit_id):
    kit = get_object_or_404(KitItem, id=kit_id)
    if request.method == "POST":
        kit.brand_name = request.POST.get('brand_name')
        kit.no_of_stock = request.POST.get('no_of_stock')
        kit.unit_price = request.POST.get('unit_price')
        kit.save()
        return redirect('kit_list')

    return render(request, 'stock/edit_kit.html', {'kit': kit})

def delete_kit(request, kit_id):
    kit = get_object_or_404(KitItem, id=kit_id)
    kit.delete()
    return redirect('kit_list')

@csrf_exempt
def item_entry(request):
    if request.method == "POST":
        itemname = request.POST.get('Item_name[]')
        purpose = request.POST.get('purpose[]')
        pieces = request.POST.get('[]')
        price=request.POST.get('price[]')
        Item_entry.objects.create(
                itemname=itemname,
                purpose=purpose,
                pieces=pieces,
                price=price
        )

        return redirect('item_entry')

    return render(request, 'stock/item_entry.html')

def item_list(request):
    items = Item_entry.objects.all()
    return render(request, 'stock/item_list.html', {'items': items})

def edit_item(request, id):
    item = get_object_or_404(Item_entry, id=id)
    if request.method == 'POST':
        item.itemname = request.POST.get('Item_name[]')
        item.pieces = request.POST.get('no_of_pieces')
        item.price = request.POST.get('price')
        item.save()
        return redirect('item_list')
    return render(request, 'stock/edit_item.html', {'item': item})

def delete_item(request, id):
    item = get_object_or_404(Item_entry, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item_list.html')

def kit_dist(request):
    admissions = AddRegister.objects.all()
    return render(request, "stock/kit_dist.html", {'admissions': admissions})


def player_details(request):
    admissions = AddRegister.objects.all()
    selected_player = None

    if 'name' in request.GET:
        selected_player = get_object_or_404(AddRegister, id=request.GET['name'])

    kits = KitItem.objects.all()
    items = Item_entry.objects.all()  # Fetch all items from the Item model

    return render(request, 'stock/kit_dist.html', {
        'admissions': admissions,
        'selected_player': selected_player,
        'kits': kits,
        'items': items  # Pass items to the template
    })

def fetch_kit_list(request):
    try:
        kits = KitItem.objects.all().values('name', 'brand_name', 'no_of_stock', 'unit_price')
        return JsonResponse({'kits': list(kits)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def fetch_item_list(request):
    items = Item_entry.objects.all().values('id', 'itemname', 'pieces', 'price')
    item_list = list(items)
    return JsonResponse({'items': item_list})




def kit_distribution_view(request):
    admissions = AddRegister.objects.all()
    selected_player = None

    if request.method == 'GET' and 'name' in request.GET:
        selected_player_id = request.GET.get('name')
        if selected_player_id:
            selected_player = AddRegister.objects.get(id=selected_player_id)

    if request.method == 'POST':
        selectCustomer = request.POST.get('selectCustomer')
        admission_no = request.POST.get('admission_no')
        phone = request.POST.get('phone')
        adhar = request.POST.get('adhar')
        place = request.POST.get('place')
        address = request.POST.get('address')
        package = request.POST.get('package')
        sessions = request.POST.get('sessions')
        batchtime = request.POST.get('batchtime')
        totalAmount = request.POST.get('totalAmount')
        balance = request.POST.get('balance')
        brand_name=request.POST.get('kit_id')
        unit_price = request.POST.get('unit_price')
        kit_quantity = request.POST.get('kit_quantity')
        kitTotalPrice = request.POST.get('kitTotalPrice')
        kitTotalAmount = request.POST.get('kitTotalAmount')
        finalAmount = request.POST.get('finalAmount')
        kit=request.POST.get('kit')

        if selectCustomer:
            kit_distribution.objects.create(
                selectCustomer=selectCustomer,
                admission_no=admission_no,
                phone=phone,
                adhar=adhar,
                place=place,
                address=address,
                package=package,
                sessions=sessions,
                batchtime=batchtime,
                totalAmount=totalAmount,
                balance=balance,
                brand_name=brand_name,
                kit_quantity=kit_quantity,
                kitTotalPrice=kitTotalPrice,
                kitTotalAmount=kitTotalAmount,
                finalAmount=finalAmount,
                kit=kit,
            )
            return redirect('home')

    context = {
        'admissions': admissions,
        'selected_player': selected_player,
        'kit': kit
    }
    return render(request, 'stock/kit_dist.html', context)


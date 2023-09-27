import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import datetime

# ----------------------------------------------authenticate, login, logout---------------------------------------------
@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {}
    return render(request, 'Admin/login_page.html', context)


def register(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # hna tanzido kol user dkhl l groupe client dericte
            # check the role
            selected_role = request.POST.get('role')
            if selected_role == '1':
                group = Group.objects.get(name='Client')
                user.groups.add(group)
                # add user to real table CLIENT
                Client.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                    password=user.password,

                )
            elif selected_role == '2':
                group = Group.objects.get(name='Organiseur')
                user.groups.add(group)
                # add user to real table user
                Organiseur.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                )

            messages.success(request, 'Account was created for '+username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'Admin/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')
# ---------------------------------------------------------ADMIN--------------------------------------------------------


@login_required(login_url='login')
@admin_only
def home_a(request):
    events = Evenment.objects.all()
    context = {'events': events,}
    return render(request, 'Admin/Events/events.html',context)


@login_required(login_url='login')
@admin_only
def home_stati(request):
    cs_no = Evenment.objects.filter(type='fistival').count()
    cs_no = int(cs_no)
    ce_no = Evenment.objects.filter(type='sport').count()
    ce_no = int(ce_no)
    se_no = Evenment.objects.filter(type='spect').count()
    se_no = int(se_no)
    sec_no = Evenment.objects.filter(type='prof').count()
    sec_no = int(sec_no)
    number_list = [cs_no, ce_no, se_no, sec_no]
    course_list = ['Fesitival', 'Sports', 'Spectacles', 'Conférences']

    m1 = Reservation.objects.filter(type_event='fistival').values('montant').distinct().count()

    m2 = Reservation.objects.filter(type_event='sport').values('montant').distinct().count()

    m3 = Reservation.objects.filter(type_event='spect').values('montant').distinct().count()
    m4 = Reservation.objects.filter(type_event='prof').values('montant').distinct().count()

    sum_f = 0
    reservations = Reservation.objects.filter(type_event='fistival')
    for reservation in reservations:
        sum_f += reservation.montant

    sum_s = 0
    reservations = Reservation.objects.filter(type_event='sport')
    for reservation in reservations:
        sum_s += reservation.montant

    sum_p = 0
    reservations = Reservation.objects.filter(type_event='spect')
    for reservation in reservations:
        sum_p += reservation.montant
        sum_p += reservation.montant

    sum_pr = 0
    reservations = Reservation.objects.filter(type_event='prof')
    for reservation in reservations:
        sum_pr += reservation.montant

    gender_list = ['Fesitival', 'Sports', 'Spectacles', 'Conférences']
    gender_number = [sum_f , sum_s, sum_p, sum_pr]
    context = {
        'course_list':course_list,
        'number_list':number_list,
        'gender_list':gender_list,
        'gender_number':gender_number}

    return render(request, 'Admin/statistics/adstatistics.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def client_a(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'Admin/Clients/clients.html', context)



# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def view_a_c(request, pk_test):
    client = Client.objects.get(id=pk_test)
    context = {'client': client}
    return render(request, 'Admin/Clients/view_client.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def view_a_e(request, pk_test):
    event = Evenment.objects.get(id=pk_test)
    context = {'event': event}
    return render(request, 'Admin/Events/view_event.html', context)


def create_client(request):
    form = CreatUserForm()
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # hna tanzido kol user dkhl l groupe client dericte
            # check the role

            group = Group.objects.get(name='Client')
            user.groups.add(group)
            # add user to real table user
            Client.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                    password=user.password,

            )
            return redirect('/admin/client/')
    context = {'form': form}
    return render(request, 'Admin/Clients/client_form.html', context)


def update_client(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    user = client.user

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            user.username = form.cleaned_data.get('name')
            user.email = form.cleaned_data.get('email')
            form.save()
            user.save()
            return redirect('/admin/client/')

    context = {
        'form': form,
    }
    return render(request, 'Admin/Clients/client_form.html', context)


def delete_client(request, pk):
    client = Client.objects.get(id=pk)

    if request.method == 'POST':
        # print('______', request.POST)
        client.user.delete()
        client.delete()
        return redirect('/admin/client/')
    context = {'form': client}
    return render(request, 'Admin/Clients/delete_client.html', context)



# Evenment


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def event_a(request):
    events = Evenment.objects.all()
    context = {'events': events}
    return render(request, 'Admin/Events/events.html', context)


def add_event_a(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            Evenment.date = form.cleaned_data['date']
            form.save()
            return redirect('events_a')
    else:
        form = CreateEventForm()
    context = {'form': form}
    return render(request, 'Admin/Events/add_event.html', context)


def delete_event_a(request, pk):
    event = Evenment.objects.get(id = pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events_a')

    context = {'form': event}
    return render(request, 'Admin/Events/delete_event.html', context)


def update_event_a(request, pk):
    event = Evenment.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST' :
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('events_a')

    context = {'form': form}
    return render(request, 'Admin/Events/event_form.html', context)


def validation(request, pk):
    event = Evenment.objects.get(id=pk)
    event.is_Vaide = True
    event.save()
    # create notification
    event = Evenment.objects.get(id=pk)
    clients = Client.objects.all()
    for client in clients:
        notification = Notification()
        notification.client = client
        notification.name_event = event.name
        notification.date_event = event.date
        notification.lieu_event = event.lieu
        # notification.vue = False ---> par defaut false
        notification.save()

    return redirect('events_a')

# ---------------------------------------------------------ORGANISEUR--------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def home_o(request):
    context = {}
    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
        context = {
            'id_org': org_id,
            'obj':organisateur
        }
    return render(request, 'Organiseurs/Events/events.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def event_o(request):
    events = Evenment.objects.all()
    context = {}
    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
        context = {
            'id_org': org_id,
            'events': events,
            'obj':organisateur

        }
    return render(request, 'Organiseurs/Events/events.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def view_o_e(request, pk_test):
    event = Evenment.objects.get(id=pk_test)
    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
    context = {'event': event, 'obj': organisateur}
    return render(request, 'Organiseurs/Events/view_event.html', context)


from .models import Evenment

@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def add_event(request):
    context = {}
    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
        if request.method == 'POST':
            form = CreateEventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.date = form.cleaned_data['date']
                event.id_organ = org_id  # Assign org_id to the id_organ attribute
                event.save()
                return redirect('events_o')
        else:
            form = CreateEventForm()

        context = {'form': form, 'obj': organisateur}
    return render(request, 'Organiseurs/Events/add_event.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def delete_event(request, pk):
    event = Evenment.objects.get(id = pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events_o')
    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
    context = {'form': event, 'obj': organisateur}
    return render(request, 'Organiseurs/Events/delete_event.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def update_event(request, pk):
    event = Evenment.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('events_o')

    if request.user.is_authenticated:
        org_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=org_id)
    context = {'form': form, 'obj': organisateur}
    return render(request, 'Organiseurs/Events/event_form.html', context)



from django.db.models import Count, Sum
from django.shortcuts import render
from .models import Reservation, Evenment


@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def statistique_org(request):
    reservations = Reservation.objects.all()
    context = {}

    debug_info = []  # Create an empty list to store the debug information

    if request.user.is_authenticated:
        org_id = request.user.id
        events = Evenment.objects.filter(id_organ=org_id)
        for event in events:
            for reservation in reservations:
                if str(event.name) == str(reservation.evenment):
                    debug_info.append({
                        'user_email': reservation.user_email,
                        'event_name': event.name,
                        'event_date': event.date,
                        'event_lieu': event.lieu,
                        'reservation_type': reservation.type_event,
                        'montant': reservation.montant
                    })

    cs_no = sum(1 for info in debug_info if info['reservation_type'] == 'fistival')
    ce_no = sum(1 for info in debug_info if info['reservation_type'] == 'sport')
    se_no = sum(1 for info in debug_info if info['reservation_type'] == 'spect')
    sec_no = sum(1 for info in debug_info if info['reservation_type'] == 'prof')
    number_list = [cs_no, ce_no, se_no, sec_no]
    course_list = ['Fesitival', 'Sports', 'Spectacles', 'Conférences']

    sum_f = sum(info['montant'] for info in debug_info if info['reservation_type'] == 'fistival')
    sum_s = sum(info['montant'] for info in debug_info if info['reservation_type'] == 'sport')
    sum_p = sum(info['montant'] for info in debug_info if info['reservation_type'] == 'spect')
    sum_pr = sum(info['montant'] for info in debug_info if info['reservation_type'] == 'prof')

    gender_list = ['Fesitival', 'Sports', 'Spectacles', 'Conférences']
    gender_number = [sum_f, sum_s, sum_p, sum_pr]

    if request.user.is_authenticated:
        user_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=user_id)
    context = {
        'course_list': course_list,
        'number_list': number_list,
        'gender_list': gender_list,
        'gender_number': gender_number,
        'obj': organisateur
    }

    return render(request, 'Organiseurs/statistics/adstatistics.html', context)

# ------------------------CLIENT-----------------------------------


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def home_c(request):
    events = Evenment.objects.all()
    current_date = datetime.date.today()
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'notif': notif, 'events': events, 'current_date': current_date}
    return render(request, 'Clients/index.html', context)

# --------------------------------------------


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def event_festival(request):
    events = Evenment.objects.all()
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'events': events, 'notif': notif}
    return render(request, 'Clients/festival.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def event_spectacle(request):
    events = Evenment.objects.all()
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'events': events, 'notif': notif}
    return render(request, 'Clients/spectacle.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def event_sport(request):
    events = Evenment.objects.all()
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'events': events, 'notif': notif}
    return render(request, 'Clients/sport.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def event_conférence(request):
    events = Evenment.objects.all()
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'events': events, 'notif': notif}
    return render(request, 'Clients/conférecne.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def buy_c(request, pk):
    event = Evenment.objects.get(id=pk)
    user = request.user
    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = 0
    notifications = Notification.objects.all()
    for notification in notifications:
        if current_client == notification.client and notification.vue == False:
            notif += 1
    # End Notification # --------------------------------------------
    context = {'event': event, 'user': user, 'notif': notif}
    return render(request, 'Clients/chose_number_ticket.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def panel(request):
    context = {}
    if request.method == 'POST':
        id_event = request.POST.get('event_name')
        event = Evenment.objects.get(id=id_event)
        user_email = request.POST.get('user_email')

        ticket_number = request.POST.get('ticket_number')

        current_date = datetime.date.today()

        # Check if the values are not None
        if event.nbr_ticket_max is not None and ticket_number is not None:
            # nombre des ticket restants
            nbr_ticket_exist = int(event.nbr_ticket_max) - int(ticket_number)
            if nbr_ticket_exist <= 0:
                return render(request, 'Clients/index.html')
            else:
                #  mis a jour des event.nbr_ticket_ma
                event.nbr_ticket_max = nbr_ticket_exist
                event.save()
                # La somme total (Montant)
                montant = float(ticket_number) * event.price

                # Create a new Reservation object and set its attributes
                reservation = Reservation()
                reservation.evenment = event
                reservation.user_email = user_email
                reservation.type_event = event.type
                reservation.nbr_ticket = ticket_number
                reservation.montant = montant
                reservation.save()
                # take reservation to use it in card autentification
                # Notification # --------------------------------------------
                current_client = request.user.client_set.first()
                notif = 0
                notifications = Notification.objects.all()
                for notification in notifications:
                    if current_client == notification.client and notification.vue == False:
                        notif += 1
                # End Notification # --------------------------------------------
                context = {
                    'event': event,
                    'user': user_email,
                    'nbr': ticket_number,
                    'montant': montant,
                    'reservation': reservation,
                    'notif': notif
                }
        else:
            return render(request, 'Clients/index.html')  # Handle the case where values are None

    return render(request, 'Clients/panel.html', context)


from django.contrib import messages


from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import messages

@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def carde_autentification(request, pk):
    current_date = datetime.date.today()
    events = Evenment.objects.all()
    context = {'events': events, 'current_date': current_date}


    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        card_number = request.POST.get('card_number')
        card_exp = request.POST.get('card_exp')
        card_cvv = request.POST.get('card_cvv')
        reservation = Reservation.objects.get(id=pk)
        print(full_name)
        print(card_number)
        print(card_exp)
        print(card_cvv)

        if int(card_cvv) == 1234:
            for ev in events:
                if ev.name == str(reservation.evenment):
                    ev.nbr_ticket_max += reservation.nbr_ticket
                    ev.save()
            reservation.delete()
            messages.error(request, 'Payment failed. Please try again.')
            return redirect('home')  # Redirect to the home page
        else:
            reservation.save()
            payment = Payment()
            payment.reservation = reservation
            payment.montant = reservation.montant
            payment.save()
            messages.success(request, 'Payment successful!')

            # Generate data for PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            XX = str(reservation.montant)+ ' Dh'
            # Write data to the PDF
            data = [
                ['User Email       ', reservation.user_email],
                ['Type Event       ', reservation.type_event],
                ['Number Tickets   ', reservation.nbr_ticket],
                ['Price            ', XX],
                ['Code Pass        ', int(reservation.id) * 15467],
            ]

            line_height = 30
            x = 100
            y = 700

            for row in data:
                label, value = row
                p.drawString(x, y, label + ':')
                p.drawString(x + 100, y, str(value))
                y -= line_height

            p.showPage()
            p.save()

            buffer.seek(0)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="payment_details.pdf"'
            response.write(buffer.getvalue())

            return response

    return render(request, 'Clients/index.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def search_events(request):
    your_search_query = request.GET.get('search')
    prix_search_query = request.GET.get('filter_by')

    results = Evenment.objects.filter(name__contains=your_search_query)

    if prix_search_query:
        if prix_search_query == 'price_0_200':
            results = results.filter(price__range=(0, 200))
        elif prix_search_query == 'price_200_500':
            results = results.filter(price__range=(200, 500))
        elif prix_search_query == 'price_500_1000':
            results = results.filter(price__range=(500, 1000))

    # Notification # --------------------------------------------
    current_client = request.user.client_set.first()
    notif = Notification.objects.filter(client=current_client, vue=False).count()
    # End Notification # --------------------------------------------

    context = {'results': results, 'notif': notif}
    print(results)
    return render(request, 'Clients/events_search.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification, Evenment

@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def notifications(request):
    notifications = Notification.objects.all()
    events = Evenment.objects.all()
    results = Notification.objects.filter(vue=False)
    current_client = request.user.client_set.first()  # Access the associated Client object

    viewed_notifications = []  # Create an empty list to store viewed notifications

    # Set vue to True for all notifications in results
    for notification in results:
        print(current_client)
        if notification.client == current_client and notification.vue == False:
            notification.vue = True
            notification.save()
            viewed_notifications.append(notification)  # Append the viewed notification to the list

    context = {'notifications': notifications, 'events': events, 'results': results, 'viewed_notifications': viewed_notifications}
    return render(request, 'Clients/events_Notification.html', context)


def clients_reservation(request):
    reservations = Reservation.objects.all()
    context = {}

    debug_info = []  # Create an empty list to store the debug information

    if request.user.is_authenticated:
        org_id = request.user.id
        events = Evenment.objects.filter(id_organ=org_id)
        organisateur = get_object_or_404(Organiseur, user=org_id)
        for event in events:
            for reservation in reservations:
                if str(event.name) == str(reservation.evenment):
                    debug_info.append({
                        'user_email': reservation.user_email,
                        'event_name': event.name,
                        'event_date': event.date,
                        'event_lieu': event.lieu,
                        'reservation_type': reservation.type_event,
                        'montant': reservation.montant
                    })


        context = {
            'id_org': org_id,
            'events': events,
            'debug_info': debug_info,  # Add the debug_info list to the context
            'obj': organisateur
        }

    return render(request, 'Organiseurs/Events/events_reservation.html', context)


from django.shortcuts import get_object_or_404


@login_required(login_url='login')
@allowed_users(allowed_roles=['Organiseur'])
def setting_organisuer(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        organisateur = get_object_or_404(Organiseur, user=user_id)
        form = SettingOrganisation(request.POST or None, request.FILES, instance=organisateur)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'obj': organisateur
    }
    return render(request, 'Organiseurs/setting/setting_organisuer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def search_events_a(request):
    your_search_query = request.GET.get('search')
    results = Evenment.objects.filter(name__contains=your_search_query)

    context = {'results': results}
    print(results)
    return render(request, 'Admin/events_search_a.html', context)




import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotel import services
from hotel.forms import LoginForm, RegisterForm


def index(request):
    return render(request=request, template_name='hotel/index.html')


def register(request):
    login_form = LoginForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            username = user.username
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            return user_login_redirect(request, user)
    else:
        register_form = RegisterForm()
    return render(request=request, template_name='hotel/signin-signup.html', context={
        'login_form': login_form,
        'register_form': register_form
    })


def login_view(request):
    if request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        return user_login_redirect(request, user)
    else:
        login_form = LoginForm(request.POST)
        register_form = RegisterForm()
        return render(request, template_name='hotel/signin-signup.html', context={
            'login_form': login_form,
            'register_form': register_form
        })


def user_login_redirect(request, user):
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('hotel:listing'))
    else:
        login_form = LoginForm(request.POST)
        login_form.add_error('', 'Username/Password is incorrect. Please try again.')
        register_form = RegisterForm()
        return render(request=request, template_name='hotel/signin-signup.html', context={
            'login_form': login_form,
            'register_form': register_form
        })


def logout_view(request):
    logout(request)
    return redirect(reverse('hotel:homepage'))


@login_required
def hotel_listing(request):
    hotels = services.get_hotel_list()
    cities = {}
    price_range = {'low': None, 'high': None}
    for hotel in hotels:
        if hotel['city'] not in cities:
            cities[hotel['city']] = 1
        else:
            cities[hotel['city']] += 1
        if price_range['low'] is None or hotel['price'] < price_range['low']:
            price_range['low'] = hotel['price']
        if price_range['high'] is None or hotel['price'] > price_range['high']:
            price_range['high'] = hotel['price']
    context = {'cities': cities, 'hotels': hotels, 'price_range': price_range}
    return render(request, template_name='hotel/listing.html', context=context)


class GetHotels(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return services.get_hotel_list()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from hotel.serializers import HotelSerializer
            hotel_name = None
            price_range = None
            dates = None
            city = None
            filtered_hotels = []
            hotels = self.get_queryset()
            get_params = request.GET
            if 'name' in get_params:
                hotel_name = get_params['name'].lower()
            if 'price' in get_params:
                price_range = get_params['price'].split(',')
            if 'date' in get_params:
                dates = get_params['date'].split(',')
                dates[0] = datetime.datetime.strptime(dates[0], '%d/%m/%Y')
                dates[1] = datetime.datetime.strptime(dates[1], '%d/%m/%Y')
            if 'city' in get_params:
                city = get_params['city'].lower()
            for hotel in hotels:
                hotel['image_url'] = get_image_url()
                if (hotel_name is None or hotel_name in hotel['name'].lower()) and (
                        price_range is None or (float(price_range[0]) <= float(hotel['price']) <= float(price_range[1]))
                        ) and (city is None or (city in hotel['city'].lower())):
                    if dates is not None:
                        availabilities = hotel['availability']
                        for availability in availabilities:
                            if dates[0] >= datetime.datetime.strptime(availability['from'], '%d-%m-%Y') and (
                                        dates[1] <= datetime.datetime.strptime(availability['to'], '%d-%m-%Y')
                            ):
                                filtered_hotels.append(hotel)
                                break
                    else:
                        filtered_hotels.append(hotel)
            if 'sort' in get_params and request.user.is_superuser:
                if get_params['order'] == 'desc' or get_params['order'] == 'asc':
                    if get_params['sort'] == 'name':
                        if get_params['order'] == 'desc':
                            filtered_hotels = sorted(filtered_hotels, key=lambda hotel_obj: hotel_obj['name'],
                                                     reverse=True)
                        elif get_params['order'] == 'asc':
                            filtered_hotels = sorted(filtered_hotels, key=lambda hotel_obj: hotel_obj['name'])
                    elif get_params['sort'] == 'price':
                        if get_params['order'] == 'desc':
                            filtered_hotels = sorted(filtered_hotels, key=lambda hotel_obj: hotel_obj['price'],
                                                     reverse=True)
                        elif get_params['order'] == 'asc':
                            filtered_hotels = sorted(filtered_hotels, key=lambda hotel_obj: hotel_obj['price'])
            serializer = HotelSerializer(filtered_hotels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


def get_image_url():
    import random
    images = [
        'https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg',
        'https://a0.muscache.com/im/pictures/21611933/43f6de69_original.jpg',
        'https://a0.muscache.com/im/pictures/65441227/bb1eb2dd_original.jpg',
        'https://a0.muscache.com/im/pictures/52149945/33130c63_original.jpg',
        'https://a0.muscache.com/im/pictures/6722906/b4bc6418_original.jpg',
        'https://a0.muscache.com/im/pictures/812e040f-6f6f-4cae-ad67-66c050b57c1f.jpg'
    ]
    return random.choice(images)

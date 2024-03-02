from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from modtmrpg import models
from modtmrpg import forms

import requests
import json

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1213447548342116373'
CLIENT_SECRET = '11ZYkGhlOqRTLXl64oPxWBOETKdoQw0m'
REDIRECT_URI = "http://128.0.0.1:8000/oauth2/discord/"


# def exchange_code(code):
#   data = {
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET,
#     'grant_type': 'authorization_code',
#     'code': code,
#     'redirect_uri': REDIRECT_URI
#   }
#   headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
#   }
#   r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
#   r.raise_for_status()
#   return r.json()

def get_token():
  data = {
    'grant_type': 'client_credentials',
    'scope': 'identify connections'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  r.raise_for_status()
  return r.json()

    
def logout_view(request):
    logout(request)
    return redirect('/') # на главную страницу сайта

@csrf_exempt
def register_view(request):
    data = {}
    if request.method == "POST":
        form = forms.ModerRegForm(request.POST)
        if form.is_valid():
            moder = form.save(commit=False)
            # moder.user = request.user
            moder.save()
            print(moder.secret_code)
            user_data = {
                'secret_code': moder.secret_code,
                'password1': moder.password1,
                'password2': moder.password2,
            }

            if user_data['password1'] != user_data['password2']:
                data['alert_text'] = 'Пароли не совпадают!'
            else:
                # try:
                    moder = models.Moder.objects.get(id=user_data['secret_code'])
                    if moder:
                        print(moder.nickname)
                        user = User.objects.create_user(username=moder.nickname)
                        user.set_password(user_data['password1'])
                        user.save()
                        print('Всё заебись брат')
                        return HttpResponseRedirect('/')
                # except Exception as e:
                #     print('не повезло')
                #     print('------------------------------------')
                #     print(e)
                #     print('------------------------------------')
                #     data['alert_text'] = 'Введите корректный код!'
                
                
    form = forms.ModerRegForm()


    return render(request, "reg.html", {"form": form, 'data': data})

def accounts_profile(request):
    return HttpResponseRedirect('/')


def index(request):
    domain = request.build_absolute_uri('/')[:-1]
    print(domain)
    if domain == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    data = {}
    data['user'] = request.user
    # data['discord_user'] = 
    return render(request, 'modtmrpg/index.html', {'data': data, 'ds_url': ds_url, })

def shop(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    data = {}
    data['user'] = request.user

    items = models.Item.objects.all()

    return render(request, 'modtmrpg/shop.html', {'data': data, 'items': items, })

def oauth2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    with open('data.json', 'w') as f:
        json.dump(get_token(), f)
    
    dataJson = dict()
    with open('data.json') as json_out:
        dataJson = json.load(json_out)
    # print(dataJson['token_type'])

    # r=requests.get("https://discordapp.com/api/users/@m", headers={"Authorization":f"Bot {dataJson["access_token"]}"})
    # r.raise_for_status()

    # code = request.GET.get('code')

    # url = 'https://discord.com/api/oauth2/token'
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }
    # data = {
    #     'client_id': REDIRECT_URI,
    #     'client_secret': CLIENT_SECRET,
    #     'grant_type': 'authorization_code',
    #     'code': code,
    #     'redirect_uri': REDIRECT_URI,
    #     'scope': 'identify guilds.join'
    # }
    # response = requests.post(url, headers=headers, data=data).json()
    # access_token = response['access_token']

    # Get the user ID from the access token
    url = 'https://discord.com/api/users/@me'
    headers = {
        'Authorization': f'Bearer {dataJson["access_token"]}'
    }
    response = requests.get(url, headers=headers).json()
    with open('user.json', 'w') as f:
        json.dump(response, f)

    ds = models.Discord.objects.create(ds_id=response['id'], username=response['username'], avatar=response['avatar'], global_name=response['global_name'],)
    ds.save()
    print(request.user.username)
    current_user = models.Moder.objects.get(nickname=request.user.username)
    current_user.discord = ds
    current_user.save()
    

    return HttpResponseRedirect('/')

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

from discord_webhook import DiscordWebhook, DiscordEmbed



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
                try:
                    moder = models.Moder.objects.get(id=user_data['secret_code'])
                    if moder.is_registered:
                        data['alert_text'] = 'Вы уже зарегистрированы!'
                    elif moder and not moder.is_registered:
                        print(moder.nickname)
                        user = User.objects.create_user(username=moder.nickname)
                        user.set_password(user_data['password1'])
                        user.save()
                        print('Всё заебись брат')
                        moder.is_registered = True
                        moder.save()
                        return HttpResponseRedirect('/')
                except Exception as e:
                    print('не повезло')
                    print('------------------------------------')
                    print(e)
                    print('------------------------------------')
                    data['alert_text'] = 'Введите корректный код!'
                
                
    form = forms.ModerRegForm()


    return render(request, "reg.html", {"form": form, 'data': data})

def accounts_profile(request):
    return HttpResponseRedirect('/')


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    categories = models.MediaCategory.objects.all()
    domain = request.build_absolute_uri('/')[:-1]
    print(domain)
    if domain == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'
    data = {}
    data['user'] = request.user
    # data['discord_user'] = 
    return render(request, 'modtmrpg/index.html', {'data': data, 'ds_url': ds_url, 'categories': categories,})

def shop(request, status=''):
    categories = models.MediaCategory.objects.all()
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    data = {}
    data['user'] = request.user

    items = models.Item.objects.all()

    if status=='success':
        data['success_text'] = 'Покупка успешна!'
    elif status=='error':
        data['alert_text'] = 'Недостаточно баллов!'

    return render(request, 'modtmrpg/shop.html', {'data': data, 'items': items, 'categories':categories, })

@csrf_exempt
def buy_item(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    username = request.user.username
    moder = models.Moder.objects.get(nickname=username)
    print(id)
    item = models.Item.objects.get(id=id)
    amount = int(request.POST.get('amount'))

    if amount <0:
        return HttpResponseRedirect('/shop/')


    if moder.balance < item.price*amount:
        return HttpResponseRedirect(f'/shop/error')
    else:
        moder.balance -= item.price*amount
        moder.save()

        curatorPex = models.Pex.objects.get(pex_name='curator')
        curatorsQuery = models.Moder.objects.filter(pex=curatorPex)

        GMPex = models.Pex.objects.get(pex_name='gm')
        GMQuery = models.Moder.objects.filter(pex=GMPex)

        StPex = models.Pex.objects.get(pex_name='StModer')
        StQuery = models.Moder.objects.filter(pex=StPex)

        tapcura = []
        tapst = []

        for curator in curatorsQuery:
            # for discord in models.Discord.objects.all():
            discords = models.Discord.objects.filter(moder=curator)
            for discord in discords:
                tapcura.append(f'<@{discord.ds_id}>')  

        for gm in GMQuery:
            # for discord in models.Discord.objects.all():
            discords = models.Discord.objects.filter(moder=gm)
            for discord in discords:
                tapst.append(f'<@{discord.ds_id}>')   
            
        for StModer in StQuery:
            # for discord in models.Discord.objects.all():
            discords = models.Discord.objects.filter(moder=StModer)
            for discord in discords:
                tapst.append(f'<@{discord.ds_id}>')     

        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1213640643558117446/5dUk-tlebu7QfT6XJ35vM7Z0vGDjhPwgwjiWYRwbY7cAnHn6NrQD_E4vrdy7qlYq-zz3")            

        if item.type == 0 or item.type == 1:
            webhook.content=''.join(tapst)
        elif item.type==2:
            webhook.content=''.join(tapcura)

        

            

        embed = DiscordEmbed(title="Покупка на сайте", description="", color="03b2f8")
        # embed.set_author(name="Author Name", url="https://github.com/lovvskillz", icon_url="https://avatars0.githubusercontent.com/u/14542790")
        # embed.set_footer(text="Embed Footer Text")
        embed.set_timestamp()
        embed.add_embed_field(name=f"Модератор:", value=f"{moder.nickname}")
        embed.add_embed_field(name=f"Купил:", value=f"{item.item_name}")
        embed.add_embed_field(name=f"В количестве:", value=f"{amount}шт.")
        # embed.add_embed_field(name="Field 3", value="amet consetetur")
        # embed.add_embed_field(name="Field 4", value="sadipscing elitr")

        webhook.add_embed(embed)
        response = webhook.execute()


        return HttpResponseRedirect(f'/shop/success')
    
def buy_item_success(request):
    data = {}
    data['success_text'] = 'Покупка успешна!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })

def buy_item_error(request):
    data = {}
    data['success_text'] = 'Недостаточно баллов!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })


def media_view(request, category):
    domain = request.build_absolute_uri('/')[:-1]
    categories = models.MediaCategory.objects.all()
    data = {}
    if category != 'None':
        current_category = models.MediaCategory.objects.get(category_folder=category)
        media = models.MediaItem.objects.filter(category=current_category)
    else:
        media = models.MediaItem.objects.filter(category=None)

    return render(request, 'modtmrpg/media.html', {'data': data, 'media': media, 'categories': categories, 'domain': domain})


@csrf_exempt
def new_file(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    data = {}
    categories = models.MediaCategory.objects.all()

    # amount = int(request.POST.get('amount'))
    if request.method == "POST":
        form = forms.AddItem(request.POST,request.FILES)
        print('хуй1')
        if form.is_valid():
            print('хуй2')
            item = form.save(commit=False)
            # moder.user = request.user
            item.save()
            print(item.media_name)
            data['success'] = True
           
    form = forms.AddItem()
    return render(request, 'modtmrpg/new_file.html', {'data': data, 'categories': categories, 'form': form, })


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

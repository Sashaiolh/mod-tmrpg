import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.core.files import File

import os

import urllib.request

from django.views.decorators.csrf import csrf_exempt

from modtmrpg import models
from modtmrpg import forms

import requests
import json

from discord_webhook import DiscordWebhook, DiscordEmbed

from django.shortcuts import redirect



API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1213447548342116373'
CLIENT_SECRET = '11ZYkGhlOqRTLXl64oPxWBOETKdoQw0m'
REDIRECT_URI = "http://128.0.0.1:8000/oauth2/discord/"


webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1213640643558117446/5dUk-tlebu7QfT6XJ35vM7Z0vGDjhPwgwjiWYRwbY7cAnHn6NrQD_E4vrdy7qlYq-zz3")   


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



def download(url, nick, folder):
    print(url)
    try:
        response = requests.head(url)
        get_response = requests.get(url,stream=True)
        # time.spleep(5)
        file_name  = f'items/{folder}/moder.{nick}.png'
        with open(file_name, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            return True
    except:
        return False


def init_data(request):
    data = {}

    data['categories'] = models.MediaCategory.objects.all()
    data['current_url'] = request.build_absolute_uri('/')
    data['domain'] = request.build_absolute_uri('/')[:-1]
    data['all_moders'] = models.Moder.objects.all()
    data['ecologs'] = models.EcoLog.objects.all()
    data['moder'] = models.Moder.objects.get(nickname=request.user.username)
    data['user'] = request.user

    
    for moder in data['all_moders']:
        if not moder.skin_valid:
            moder.skin_valid = download(f'https://mcskill.net/MineCraft/?name={moder.nickname}&mode=1.png', moder.nickname, 'moderSkins')
            moder.save()
        if not moder.head_valid:
            moder.head_valid = download(f'https://mcskill.net/MineCraft/?name={moder.nickname}&mode=5&fx=43&fy=43', moder.nickname, 'moderHeads')
            moder.save()




    return data

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

@csrf_exempt
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

                        # auto-login after registration
                        new_user = authenticate(username=moder.nickname, password=user_data['password1'],)
                        login(request, new_user)


                        return HttpResponseRedirect('/')
                except Exception as e:
                    print('не повезло')
                    print('------------------------------------')
                    print(e)
                    print('------------------------------------')
                    data['alert_text'] = 'Введите корректный код!'
                
                
    form = forms.ModerRegForm()


    return render(request, "reg.html", {"form": form, 'data': data})

@csrf_exempt
def accounts_profile(request):
    return HttpResponseRedirect('/')

@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    data = init_data(request)
    print(data['domain'])
    if data['domain'] == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'
    data['user'] = request.user
    # data['discord_user'] = 
    return render(request, 'modtmrpg/index.html', {'data': data, 'ds_url': ds_url,})

@csrf_exempt
def shop(request, status=''):
    data = init_data(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    items = models.Item.objects.all()

    if status=='success':
        data['success_text'] = 'Покупка успешна!'
    elif status=='error':
        data['alert_text'] = 'Недостаточно баллов!'

    return render(request, 'modtmrpg/shop.html', {'data': data, 'items': items,})

@csrf_exempt
def modsEdit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)

    moders = models.Moder.objects.all()

    if request.method == 'POST':
        if request.POST.get('options-operator') != None:
            moder = models.Moder.objects.get(nickname=request.POST.get('nick'))
            operator = request.POST.get('options-operator')
            amount = int(request.POST.get('amount'))
            reason = request.POST.get('reason')
            if data['moder'].pex.hierarchy > moder.pex.hierarchy:
                if operator == '=':
                    moder.balance = amount
                    moder.save()
                elif operator == '-' or operator == '+':
                    amount = (-1)*amount if operator == '-' else amount
                    moder.balance += amount
                    moder.save()
                    new_log = models.EcoLog.objects.create(admin=data['moder'], moder=moder, amount=amount, reason=reason)
                    new_log.save()
        
        if request.POST.get('typePost') != None:
            moder = models.Moder.objects.get(nickname=request.POST.get('nick'))
            if (request.POST.get('typePost') == 'downmoder' and data['moder'].pex.hierarchy > moder.pex.hierarchy and (moder.pex.hierarchy > 1)) or (request.POST.get('typePost') == 'upmoder' and data['moder'].pex.hierarchy > moder.pex.hierarchy+1): 
                new_hierarchy = moder.pex.hierarchy - 1 if request.POST.get('typePost') == 'downmoder' else moder.pex.hierarchy + 1
                new_pex = models.Pex.objects.get(hierarchy=new_hierarchy)
                moder.pex = new_pex
                moder.save()
            if (request.POST.get('typePost') == 'kickmoder') and (data['moder'].pex.hierarchy > moder.pex.hierarchy):
                embed = DiscordEmbed(title="Снятие модератора", description="", color="ff0000")
                # embed.set_author(name="Author Name", url="https://github.com/lovvskillz", icon_url="https://avatars0.githubusercontent.com/u/14542790")
                # embed.set_footer(text="Embed Footer Text")
                embed.set_timestamp()
                embed.add_embed_field(name=f"Сотрудник", value=f"`{data['moder'].nickname}`")
                embed.add_embed_field(name=f"Снял", value=f"`{moder.nickname}`")
                embed.add_embed_field(name=f"С должности", value=f"{moder.pex.display_name}")
                embed.add_embed_field(name=f"Накопленные баллы", value=f"{moder.balance}")
                embed.add_embed_field(name=f"Выговоры", value=f"0/3")
                # embed.add_embed_field(name="Field 3", value="amet consetetur")
                # embed.add_embed_field(name="Field 4", value="sadipscing elitr")

                webhook.add_embed(embed)
                response = webhook.execute()

                try:
                    u = User.objects.get(username = moder.nickname)
                    u.delete()
                except:
                    pass
                moder.delete()
            
        return redirect(f'{data["current_url"]}modsEdit/')
                


    return render(request, 'modtmrpg/modsEdit.html', {'data': data, 'moders': moders,})

@csrf_exempt
def buy_item(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
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

        if item.type == 0 or item.type == 1:
            webhook.content=''.join(tapst)
        elif item.type==2:
            webhook.content=''.join(tapcura)
            

        embed = DiscordEmbed(title="Покупка на сайте", description="", color="03b2f8")
        # embed.set_author(name="Author Name", url="https://github.com/lovvskillz", icon_url="https://avatars0.githubusercontent.com/u/14542790")
        # embed.set_footer(text="Embed Footer Text")
        embed.set_timestamp()
        embed.add_embed_field(name=f"Модератор:", value=f"`{moder.nickname}`")
        embed.add_embed_field(name=f"Купил:", value=f"`{item.item_name}`")
        embed.add_embed_field(name=f"В количестве:", value=f"`{amount}шт.`")
        # embed.add_embed_field(name="Field 3", value="amet consetetur")
        # embed.add_embed_field(name="Field 4", value="sadipscing elitr")

        webhook.add_embed(embed)
        response = webhook.execute()


        return HttpResponseRedirect(f'/shop/success')

@csrf_exempt
def buy_item_success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    data = init_data(request)
    data['success_text'] = 'Покупка успешна!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })

@csrf_exempt
def buy_item_error(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    data = init_data(request)
    data['success_text'] = 'Недостаточно баллов!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })

@csrf_exempt
def media_view(request, category):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    data = init_data(request)
    if not data['moder'].is_st() and not data['moder'].is_admin():
        return HttpResponseRedirect('/')
    if category != 'None':
        current_category = models.MediaCategory.objects.get(category_folder=category)
        media = models.MediaItem.objects.filter(category=current_category)
    else:
        media = models.MediaItem.objects.filter(category=None)

    return render(request, 'modtmrpg/media.html', {'data': data, 'media': media,})


@csrf_exempt
def new_file(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
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






@csrf_exempt
def skinfix(request, nick):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    data = init_data(request)
    moder = models.Moder.objects.get(nickname=nick)
    moder.skin_valid = False
    moder.head_valid = False
    moder.save()
    return HttpResponseRedirect('/')


def oauth2Remove(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    data = init_data(request)
    if data['moder'].discord:
        data['moder'].discord.delete()
    return HttpResponseRedirect('/')


@csrf_exempt
def oauth2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
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

import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import codecs


from django import template
register = template.Library()

from django.core.files import File

import os
import os.path

import urllib.request

from django.views.decorators.csrf import csrf_exempt

from modtmrpg import models
from modtmrpg import forms

import requests
import json

import base64

from discord_webhook import DiscordWebhook, DiscordEmbed

from django.shortcuts import redirect



API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1213447548342116373'
CLIENT_SECRET = '11ZYkGhlOqRTLXl64oPxWBOETKdoQw0m'
REDIRECT_URI = "http://128.0.0.1:8000/oauth2/discord/"






class Webhook():
    def __init__(self, request):
        if request.build_absolute_uri('/')[:-1] == 'http://127.0.0.1:8000':
            self.webhookUrl = 'https://discord.com/api/webhooks/1213640643558117446/5dUk-tlebu7QfT6XJ35vM7Z0vGDjhPwgwjiWYRwbY7cAnHn6NrQD_E4vrdy7qlYq-zz3'
        else:
            self.webhookUrl = 'https://discord.com/api/webhooks/1217123338753933352/tFgGpj921OWFiEMmrbbsyHyEWGaCl7L3GbwM2fPeDcC43J8oBReFRKF7V1QJ-aJpnDW-'
    
        self.content = []

        self.webhook = DiscordWebhook(url=self.webhookUrl)
    
    def addContent(self, content):
        self.content.append(content)

    def sendEmbedWithContent(self, title, color, data, description=""):
        self.embed = DiscordEmbed(title=title, description=description, color=color)
        self.embed.set_timestamp()
        for key in data:
            self.embed.add_embed_field(name=key, value=data[key])

    # self.webhook.remove_embeds()
        self.webhook.content = ''.join(self.content)
        self.webhook.add_embed(self.embed)
        self.webhook.execute()
    
        

    




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
    response = requests.head(url)
    get_response = requests.get(url,stream=True)
    # time.spleep(5)
    file_name  = f'items/{folder}/moder.{nick}.png'
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        return True
    
def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return base64.b64encode(img).decode('utf-8')

def get_amount_of_reprimands(nick):
    moder = models.Moder.objects.get(nickname=nick)
    return len(models.Reprimand.objects.filter(moder=moder))

def init_data(request):

    data = {}

    data['categories'] = models.MediaCategory.objects.all()
    data['current_url'] = request.build_absolute_uri('/')
    data['domain'] = request.build_absolute_uri('/')[:-1]
    data['all_moders'] = models.Moder.objects.all()
    data['ecologs'] = models.EcoLog.objects.all()
    data['moder'] = models.Moder.objects.get(nickname=request.user.username)
    data['profile_moder'] = data['moder']
    data['user'] = request.user

    data['updateSkin'] = False


    
    for moder in data['all_moders']:
        if not moder.skin_valid or not os.path.isfile("items/moderSkins/moder.{nick}.png".format(nick=moder.nickname)):
            data['updateSkin'] = True
            data['updateModer'] = moder.nickname
            moder.skin_valid = True
            moder.save()
            return data
        # if not os.path.isfile("items/moderSkins/moder.{nick}.png".format(nick=moder.nickname)):
        #     data['updateSkin'] = True
        #     data['updateModer'] = moder
            
            # moder.skin_valid = download(f'https://skins.mcskill.net/MinecraftSkins/{moder.nickname}.png', moder.nickname, 'moderSkins')
            

            
    try:
        # data['skin_bust_url'] = f'https://visage.surgeplay.com/bust/256/{image_to_data_url("items/moderSkins/moder.{nick}.png".format(nick=moder.nickname))}'
        data['skin_full_url'] = f'https://visage.surgeplay.com/full/384/{image_to_data_url("items/moderSkins/moder.{nick}.png".format(nick=moder.nickname))}'
    except:
        pass
        # if not moder.head_valid:
        #     moder.head_valid = download(f'https://mcskill.net/MineCraft/?name={moder.nickname}&mode=5&fx=43&fy=43', moder.nickname, 'moderHeads')
        #     moder.save()

    return data



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
                        user = User.objects.create_user(username=moder.nickname)
                        user.set_password(user_data['password1'])
                        user.save()
                        moder.is_registered = True
                        moder.save()

                        # auto-login after registration
                        new_user = authenticate(username=moder.nickname, password=user_data['password1'],)
                        login(request, new_user)
                    return HttpResponseRedirect('/')
                except Exception as e:
                    data['alert_text'] = 'Введите корректный код!'
                
    # return HttpResponseRedirect('/')       

def newModer(request, id):
    form = forms.ModerRegForm()
    return render(request, "reg.html", {"form": form, 'id':id, })

@csrf_exempt
def accounts_profile(request):
    return HttpResponseRedirect('/')

@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    if data['domain'] == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'
    data['user'] = request.user
    # data['discord_user'] = 
    return render(request, 'modtmrpg/index.html', {'data': data, 'ds_url': ds_url,})

@csrf_exempt
def profile(request, nick=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    if data['domain'] == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'
    nickname = request.user.username if not nick else nick
    data['moder'] = models.Moder.objects.get(nickname=nickname)
    return render(request, 'modtmrpg/profile.html', {'data': data, 'ds_url': ds_url, })

@csrf_exempt
def ecoLogs(request, nick=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    if data['domain'] == 'http://127.0.0.1:8000':
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Fdiscord&scope=guilds+identify'
    else:
        ds_url = 'https://discord.com/oauth2/authorize?client_id=1213447548342116373&response_type=code&redirect_uri=http%3A%2F%2Fmodtmrpg.pythonanywhere.com%2Foauth2%2Fdiscord&scope=guilds+identify'

    return render(request, 'modtmrpg/ecoLogs.html', {'data': data, 'ds_url': ds_url, })

@csrf_exempt
def shop(request, status=''):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

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
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")
    
    if not (data['moder'].is_st() or data['moder'].is_admin()):
        return HttpResponseRedirect('/')
    
    def test(str):
        print(str, 'world!')

    moders = models.Moder.objects.all()

    if request.method == 'POST' and (data['moder'].is_st() or data['moder'].is_admin()):
        if request.POST.get('options-operator') != None:
            moder = models.Moder.objects.get(nickname=request.POST.get('nick'))
            operator = request.POST.get('options-operator')
            amount = int(request.POST.get('amount'))
            reason = request.POST.get('reason')
            if data['moder'].pex.hierarchy > moder.pex.hierarchy or request.user.is_superuser:
                if operator == '=':
                    moder.balance = amount
                    moder.save()
                elif operator == '-' or operator == '+' and amount > 0:
                    amount = (-1)*amount if operator == '-' else amount
                    moder.balance += amount
                    moder.save()
                    new_log = models.EcoLog.objects.create(admin=data['moder'], moder=moder, amount=amount, reason=reason)
                    new_log.save()
        
        if request.POST.get('typePost') != None:

            if (request.POST.get('typePost') == 'newmoder'):
                nickname = request.POST.get('nickname')
                new_moder = models.Moder.objects.create(nickname = nickname)
                new_moder.save()
                return HttpResponseRedirect('/modsEdit/')
                # return render(request, 'modtmrpg/newModer.html', {'data': data, 'moder': new_moder})

            moder = models.Moder.objects.get(nickname=request.POST.get('nick'))
            if ( (request.POST.get('typePost') == 'downmoder') and (data['moder'].pex.hierarchy > moder.pex.hierarchy and (moder.pex.hierarchy > 1) or (request.user.is_superuser and moder.pex.hierarchy > 0)) ) or (request.POST.get('typePost') == 'upmoder' and ((data['moder'].pex.hierarchy > moder.pex.hierarchy+1 and moder.pex.hierarchy > 0) or (request.user.is_superuser and moder.pex.hierarchy >= 0))): 
                new_hierarchy = moder.pex.hierarchy - 1 if request.POST.get('typePost') == 'downmoder' else moder.pex.hierarchy + 1
                new_pex = models.Pex.objects.get(hierarchy=new_hierarchy)
                moder.pex = new_pex
                moder.save()
            if (request.POST.get('typePost') == 'kickmoder') and ((data['moder'].pex.hierarchy > moder.pex.hierarchy) or request.user.is_superuser):
                
                # embed.set_author(name="Author Name", url="https://github.com/lovvskillz", icon_url="https://avatars0.githubusercontent.com/u/14542790")
                # embed.set_footer(text="Embed Footer Text")

                newEmbedData = {
                    'Сотрудник': f"`{data['moder'].nickname}`",
                    'Снял': f"`{moder.nickname}`",
                    'С должности': f"{moder.pex.display_name}",
                    'Накопленные баллы': f"{moder.balance}",
                    'Выговоры': f"{len(moder.get_all_reprimands())}/3",
                }


                try:
                    u = User.objects.get(username = moder.nickname)
                    u.delete()
                except:
                    pass
                moder.delete()
                
                webhook = Webhook(request)
                webhook.sendEmbedWithContent(title="Снятие модератора", color="ff0000", data=newEmbedData)
            
        if int(request.POST.get('is_reprimand')) == 1:
            moder = models.Moder.objects.get(nickname=request.POST.get('nick'))
            admin = data['moder']
            if admin.pex.hierarchy <= moder.pex.hierarchy:
                return redirect(f'{data["current_url"]}modsEdit/')
            reason = request.POST.get('reason')  
            new_reprimand = models.Reprimand.objects.create(admin=admin, moder=moder, reason=reason)
            new_reprimand.save()

        return redirect(f'{data["current_url"]}modsEdit/')
                


    return render(request, 'modtmrpg/modsEdit.html', {'data': data, 'moders': moders, 'test': test, 'edit': True})

@csrf_exempt
def modsList(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")
    
    def test(str):
        print(str, 'world!')

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
                


    return render(request, 'modtmrpg/modsList.html', {'data': data, 'moders': moders, 'test': test, 'edit': False, })

@csrf_exempt
def buy_item(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    username = request.user.username
    moder = models.Moder.objects.get(nickname=username)
    item = models.Item.objects.get(id=id)
    amount = int(request.POST.get('amount'))

    if amount <1:
        return HttpResponseRedirect('/shop/')


    if moder.balance < item.price*amount:
        return HttpResponseRedirect(f'/shop/error')
    else:
        moder.balance -= item.price*amount
        moder.save()

        cost = item.price*amount

        new_log = models.EcoLog.objects.create(moder=moder, amount=cost*(-1), reason=f'Покупка {"x"+str(amount) if amount != 1 else ""} {item.item_name}')
        new_log.save()

        curatorPex = models.Pex.objects.get(pex_name='curator')
        curatorsQuery = models.Moder.objects.filter(pex=curatorPex)

        GMPex = models.Pex.objects.get(pex_name='gm')
        GMQuery = models.Moder.objects.filter(pex=GMPex)

        StPex = models.Pex.objects.get(pex_name='StModer')
        StQuery = models.Moder.objects.filter(pex=StPex)


        webhook = Webhook(request)


        if int(item.type) < 3:
            for StModer in StQuery:
                discords = models.Discord.objects.filter(moder=StModer)
                for discord in discords:
                    webhook.addContent(f'<@{discord.ds_id}>') 
            
            for gm in GMQuery:
                discords = models.Discord.objects.filter(moder=gm)
                for discord in discords:
                    webhook.addContent(f'<@{discord.ds_id}>')    


        if int(item.type) >= 3:
            for curator in curatorsQuery:
                discords = models.Discord.objects.filter(moder=curator)
                for discord in discords:
                    webhook.addContent(f'<@{discord.ds_id}>')

        newEmbedData = {
            'Модератор:': f"`{moder.nickname}`",
            'Купил:': f"`{item.item_name}`",
            'В количестве:': f"`{amount}шт.`",
            'Цена:': f"`{item.price}б.`",
            'Общая стоимость:': f"`{cost}б.`",
        }

        webhook.sendEmbedWithContent(title="Покупка на сайте", color="03b2f8", data=newEmbedData)


        return HttpResponseRedirect(f'/shop/success')

@csrf_exempt
def buy_item_success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    data['success_text'] = 'Покупка успешна!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })

@csrf_exempt
def buy_item_error(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    data['success_text'] = 'Недостаточно баллов!'
    return render(request, 'modtmrpg/shop.html', {'data': data, })

@csrf_exempt
def media_view(request, category):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

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
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer'].nickname}/")

    categories = models.MediaCategory.objects.all()

    # amount = int(request.POST.get('amount'))
    if request.method == "POST":
        form = forms.AddItem(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # moder.user = request.user
            item.save()
            data['success'] = True
           
    form = forms.AddItem()
    return render(request, 'modtmrpg/new_file.html', {'data': data, 'categories': categories, 'form': form, })






@csrf_exempt
def skinfix(request, nick):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')

    moder = models.Moder.objects.get(nickname=nick)
    moder.skin_valid = False
    moder.head_valid = False
    moder.save()

    data = init_data(request)

    return HttpResponseRedirect('/')

def get_shop_items(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.user.is_superuser:
        
        f = codecs.open('get_items.json', encoding='utf-8')
        data = json.load(f)

        all_items = data['result']
        
        for item in models.Item.objects.filter(is_auto=1):
            item.delete()

        for item in all_items:
            price = int(item['pricerub'].split('.')[0])
            new_price = price/4
            if price != 0:
                name = item['name'] if int(item['amount']) == 1 else f"x{int(item['amount'])} {item['name']}"
                new_item = models.Item.objects.create(item_name=name, description='Выдаётся старшим мод. составом', note='Запрещена продажа и передача!',price=new_price, is_auto=1, image_url=item['img'])
                new_item.save()
    return HttpResponse('done')

def api_OC_moders(request):

    content = []

    for moder in list(models.Moder.objects.all())[:-1]:
        string = str()
        moderContent = {
            'nickname': moder.nickname,
            'discord': moder.discord.username if moder.discord else "",
            'pex': moder.pex.display_name,
            'prefix_color': hex(int(moder.pex.prefix_color[1:], 16)),
            'nickname_color': hex(int(moder.pex.OC_nickname_color[1:], 16)),
        }
        for key in moderContent:
            value = f'"{moderContent[key]}"' if (type(moderContent[key]) is str and (str(moderContent[key])[:2]!='0x')) else f'{moderContent[key]}'
            string += '{key} = {value}, '.format(key=key, value=value)
        resultString = '{' + string + '}, '
        content.append(resultString)
    # result = 'local moders = {\n' + '\n'.join(content) + '\n' + '}'
    result = 'moders = {\n' + '\n'.join(content) + '\n' + '}'
    return HttpResponse(result, content_type='text/plain; charset=utf-8')



def api_OC_config(request, configName):
    config = models.Config.objects.get(config_name=configName)
    return HttpResponse(config.config, content_type='text/plain; charset=utf-8')

def EnigmaConfig(request, configName):
    config = models.EnigmaConfig.objects.get(config_name=configName)
    return HttpResponse(config.config, content_type='text/plain; charset=utf-8')



def bonus(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    data = init_data(request)

    if request.method == 'POST':
        if request.POST.get('postType') == 'change_amount':
            new_amount = request.POST.get('amount')
            bonus_request_id = request.POST.get('bonus_request_id')
            if data['moder'].is_st() or data['moder'].is_admin() or request.user.is_superuser:
                bonus_request = models.BonusRequest.objects.get(id=bonus_request_id)
                if not new_amount:
                    new_amount = None
                bonus_request.final_amount = new_amount
                bonus_request.save()

        if request.POST.get('postType') == 'process_request':
            bonus_request_id = request.POST.get('bonus_request_id')
            if data['moder'].is_st() or data['moder'].is_admin() or request.user.is_superuser:
                bonus_request = models.BonusRequest.objects.get(id=bonus_request_id)
                if bonus_request.is_accepted() == False:
                    if request.POST.get('request_action') == 'cancel':
                        bonus_request.is_canceled = True
                    elif request.POST.get('request_action') == 'accept':
                        bonus_request.is_canceled = False
                        amount = bonus_request.final_amount if bonus_request.final_amount else bonus_request.request_amount
                        new_log = models.EcoLog.objects.create(moder=bonus_request.moder,admin=data['moder'], amount=amount,
                                                               reason=f'{bonus_request.title} (auto)')
                        new_log.save()
                        bonus_request.moder.balance += amount
                        bonus_request.moder.save()
                    bonus_request.who_accepted = data['moder']
                    bonus_request.save()


    my_bonus_requests = models.BonusRequest.objects.filter(moder=data['moder']).order_by('moder')

    all_bonus_requests = models.BonusRequest.objects.all()

    return render(request, 'modtmrpg/bonus.html', {'data': data, 'my_bonus_requests': my_bonus_requests, 'all_bonus_requests': all_bonus_requests, })

def add_bonus_request(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    data = init_data(request)

    if request.method == 'GET':
        print(56456454612321312321213213213213213)
        if request.GET.get('getType') == 'add_bonus_request':
            print(12312312321312321213213213213213)
            title = request.GET.get('title')
            description = request.GET.get('description')
            request_amount = request.GET.get('request_amount')

            new_bonus_request = models.BonusRequest.objects.create(title=title, description=description,
                                                                   request_amount=request_amount, moder=data['moder'])
            new_bonus_request.save()
            return HttpResponseRedirect('/bonus/')
    return HttpResponseRedirect('/bonus/')


# def api_OC_moders(request):

#     content = []

#     for moder in list(models.Moder.objects.all())[:-1]:
#         string = str()
#         moderContent = {
#             'nickname': moder.nickname,
#             'discord': moder.discord.username if moder.discord else "",
#             'pex': moder.pex.display_name,
#             'prefix_color': hex(int(moder.pex.prefix_color[1:], 16)),
#             'end': True,
#         }
#         for key in moderContent:
#             value = f'"{moderContent[key]}"' if (type(moderContent[key]) is str and (str(moderContent[key])[:2]!='0x')) else f'{moderContent[key]}'
#             if key == 'end':
#                 string = string[:-2]
#             else:
#                 string += '{key} = {value}, '.format(key=key, value=value)
#         resultString = '{' + string + '}, '
#         content.append(resultString)
#     # result = 'local moders = {\n' + '\n'.join(content) + '\n' + '}'
#     result = '{' + ''.join(content)[:-5] + '}}'
#     return HttpResponse(result, content_type='text/plain; charset=utf-8')









# def get_token(code):
#   data = {
#     'client_id': '1213447548342116373',
#     'client_secret': CLIENT_SECRET,
#     'grant_type': 'authorization_code',
#     'code': code,
#   }
#   headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
#   }
#   r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
#   r.raise_for_status()
#   return r.json()


@csrf_exempt
def oauth2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.build_absolute_uri('/')[:-1] == 'http://127.0.0.1:8000':
        REDIRECT_URI = 'http://127.0.0.1:8000/oauth2/discord'
    else:
        REDIRECT_URI = 'http://modtmrpg.pythonanywhere.com/oauth2/discord'


    code = request.GET.get('code')

    url = 'https://discord.com/api/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify guilds.join'
    }
    token_data = requests.post(url, headers=headers, data=data).json()

    # Get the user ID from the access token
    url = 'https://discord.com/api/users/@me'
    headers = {
        'Authorization': f'Bearer {token_data["access_token"]}'
    }

    response = requests.get(url, headers=headers).json()

    ds = models.Discord.objects.create(ds_id=response['id'], username=response['username'], avatar=response['avatar'], global_name=response['global_name'],)
    ds.save()
    current_user = models.Moder.objects.get(nickname=request.user.username)
    current_user.discord = ds
    current_user.save()
    

    return HttpResponseRedirect('/')


def oauth2Remove(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    data = init_data(request)
    if data['updateSkin']:
        return HttpResponseRedirect(f"https://mod-tmrpg.vercel.app/updateSkin/{data['updateModer']}/")

    if data['moder'].discord:
        data['moder'].discord.delete()
    return HttpResponseRedirect('/')


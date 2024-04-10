from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import ast


from modtmrpg.models import Moder, Config, Pex

pexs = {
    'Гл.Модератор': 'gm',
    'Ст.Модератор': 'StModer',
    'Модератор': 'moder',
    'Помощник': 'helper2',
    'Стажер': 'helper1',
}
class Moder():
    def __init__(self, data, playtimeMins):
        self.nickname = data['nickname']
        if data['prefix'] in pexs.keys():
            self.pex = data['prefix']
            print(self.pex)
            self.pexObj = Pex.objects.get(pex_name=pexs[data['prefix']])
        else:
            self.pex = None
        self.minutesStart = int(data['playtime1'])*60 + (int(data['playtime2'])/100)*60
        self.minutesEnd = playtimeMins

    def getCurrentPlaytime(self):
        return round(float((self.minutesEnd-self.minutesStart)/60), 2)

    def getModer(self):
        if self.pex:
            return {
                'nickname': self.nickname,
                'pex': self.pex,
                'prefix_color': hex(int(self.pexObj.prefix_color[1:], 16)),
                'nickname_color': hex(int(self.pexObj.OC_nickname_color[1:], 16)),
                'currentplaytime': self.getCurrentPlaytime()
            }
        else:
            return None


@csrf_exempt
def api_macrokb_playtimereport(request):
    config = Config.objects.get(config_name='playtimeTest')
    if request.method == 'POST':
        text1 = str(request.body)[2:]
        text = text1[:-1]
        config.config = text
        config.save()
    return HttpResponse('huy huy huy huy', content_type='text/plain; charset=utf-8')

@csrf_exempt
def api_macrokb_oc_pushplaytimes(request):
    config = Config.objects.get(config_name='playtimes')
    if request.method == 'POST':
        text1 = str(request.body)[2:]
        text = text1[:-1]
        config.config = text
        config.save()
    return HttpResponse('huy huy huy huy', content_type='text/plain; charset=utf-8')

@csrf_exempt
def api_macrokb_oc_moderslist(request):
    config = Config.objects.get(config_name='playtimeTest')
    allModersJsons = config.config.split('|')[:-1]
    content = []


    for moderJson in allModersJsons:
        dictionary = ast.literal_eval(moderJson)
        # Декодирование поля prefix с учетом предполагаемой кодировки UTF-8
        decoded_prefix = dictionary['prefix'].encode('latin1').decode('utf-8')
        # Замена декодированного значения в словаре
        dictionary['prefix'] = decoded_prefix.replace('[', '').replace(']', '')

        newModer = {
            'nickname': dictionary['nickname']
        }

        string = str()

        if newModer:
            for key in newModer:
                value = f'"{newModer[key]}"' if (type(newModer[key]) is str and (
                        str(newModer[key])[:2] != '0x')) else f'{newModer[key]}'
                string += '{key} = {value}, '.format(key=key, value=value)
            resultString = '{' + string + '}, '
            content.append(resultString)
    result = 'moderslist = {\n' + '\n'.join(content) + '\n' + '}'
    return HttpResponse(result, content_type='text/plain; charset=utf-8')

def api_macrokb_getPlayTimeReport(request):
    config = Config.objects.get(config_name='playtimeTest')
    playtimeConfig = Config.objects.get(config_name='playtimes')
    allModersJsons = config.config.split('|')[:-1]
    content = []

    playtimes = {}
    for moder in playtimeConfig.config.split('|')[:-1]:
        playtimes[moder.split(';')[0]] = [moder.split(';')[1], moder.split(';')[2]]

    for moderJson in allModersJsons:
        print('-----')
        dictionary = ast.literal_eval(moderJson)

        # Декодирование поля prefix с учетом предполагаемой кодировки UTF-8
        decoded_prefix = dictionary['prefix'].encode('latin1').decode('utf-8')

        # Замена декодированного значения в словаре
        dictionary['prefix'] = decoded_prefix.replace('[', '').replace(']', '')

        print(dictionary)

        playtimemins = playtimes[dictionary['nickname']][0]*60 + playtimes[dictionary['nickname']][1]

        newModer = Moder(dictionary, playtimemins).getModer()
        print(newModer)

        string = str()

        if newModer:
            for key in newModer:
                value = f'"{newModer[key]}"' if (type(newModer[key]) is str and (
                        str(newModer[key])[:2] != '0x')) else f'{newModer[key]}'
                string += '{key} = {value}, '.format(key=key, value=value)
            resultString = '{' + string + '}, '
            content.append(resultString)
        # result = 'local moders = {\n' + '\n'.join(content) + '\n' + '}'
    result = 'moders = {\n' + '\n'.join(content) + '\n' + '}'
    return HttpResponse(result, content_type='text/plain; charset=utf-8')


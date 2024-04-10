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
    def __init__(self, data):
        self.nickname = data['nickname']
        if data['prefix'] in pexs.keys():
            self.pex = data['prefix']
            print(self.pex)
            self.pexObj = Pex.objects.get(pex_name=pexs[data['prefix']])
        else:
            self.pex = None
        self.minutesStart = data['playtime1']*60 + (data['playtime2']/100)*60
        self.minutesEnd = data['hours']*60 + data['minutes']

    def getCurrentPlaytime(self):
        return round(float((self.minutesEnd-self.minutesStart)/60), 2)

    def getModer(self):
        if self.pex:
            return {
                'nickname': self.nickname,
                'pex': self.pex,
                'currentplaytime': str(self.getCurrentPlaytime()),
                'prefix_color': hex(int(self.pexObj.prefix_color[1:], 16)),
                'nickname_color': hex(int(self.pexObj.nickname_color[1:], 16)),
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

def api_macrokb_getPlayTimeReport(request):
    config = Config.objects.get(config_name='playtimeTest')
    allModersJsons = config.config.split('|')[:-1]
    content = []
    for moderJson in allModersJsons:
        print('-----')
        dictionary = ast.literal_eval(moderJson)

        # Декодирование поля prefix с учетом предполагаемой кодировки UTF-8
        decoded_prefix = dictionary['prefix'].encode('latin1').decode('utf-8')

        # Замена декодированного значения в словаре
        dictionary['prefix'] = decoded_prefix.replace('[', '').replace(']', '')

        print(dictionary)

        newModer = Moder(dictionary).getModer()
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


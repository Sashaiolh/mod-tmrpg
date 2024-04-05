from django.http import HttpResponse, HttpResponseRedirect
from modtmrpg.models import Moder, Config
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_macrokb_playtimereport(request):
    if request.method == 'POST':
        text = str(request.body)
        config = Config.objects.get(config_name='playtimeTest')
        config.config = text
        config.save()
    return HttpResponse('huy huy huy huy', content_type='text/plain; charset=utf-8')

def api_macrokb_getPlayTimeReport(request):
    content = []
    for moder in list(Moder.objects.all())[:-1]:
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


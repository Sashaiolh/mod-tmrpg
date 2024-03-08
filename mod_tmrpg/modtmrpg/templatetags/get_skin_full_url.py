from .utils import image_to_data_url

from django import template
register = template.Library()

@register.filter()
def get_skin_full_url(nick):
    if nick == 'default':
        return f'https://visage.surgeplay.com/full/384/{image_to_data_url("items/default.png")}'
    try:
        return f'https://visage.surgeplay.com/full/384/{image_to_data_url("items/moderSkins/moder.{nick}.png".format(nick=nick))}'
    except:
        return f'https://visage.surgeplay.com/full/384/{image_to_data_url("items/default.png")}'
    
from .utils import image_to_data_url

from django import template
register = template.Library()

@register.filter()
def get_skin_face_url(nick):
    if nick == 'default':
        return f'https://visage.surgeplay.com/face/256/{image_to_data_url("items/default.png")}'
    return f'https://visage.surgeplay.com/face/256/{image_to_data_url("items/moderSkins/moder.{nick}.png".format(nick=nick))}'
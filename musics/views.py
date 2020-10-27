import json
from django.http.response import HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from .models import Music

# Create your views here.
@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        musics = Music.objects.values()
        musics_data = json.dumps([music for music in musics])
        return HttpResponse(musics_data, content_type='application/json')
    else:
        music = Music()
        received_json_data = json.loads(request.body.decode('utf-8')) 
        music.singer = received_json_data.get('singer')
        music.title = received_json_data.get('title')
        music.youtube_url = received_json_data.get('youtube_url')
        music.save()
        return HttpResponse(json.dumps(model_to_dict(music)), content_type='application/json')

@require_http_methods(['GET'])
def random(request):
    music = Music.objects.order_by('?').first()
    return HttpResponse(json.dumps(model_to_dict(music)), content_type='application/json')
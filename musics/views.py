import random
from django.shortcuts import redirect, render
from django.db.models import Max
from .models import Music
from .forms import MusicForm
# Create your views here.
def index(request):
    max_id = Music.objects.all().aggregate(max_id = Max("id"))['max_id']
    while True : 
        pk = random.randint(1, max_id)
        music = Music.objects.filter(pk=pk).first()
        if music : 
            context = {
                'music': music,
            }
            return render(request, 'musics/index.html', context)
    # music = Music.objects.get(pk=1)


# https://youtu.be/MzF5bWjKjjI 벚꽃엔딩
# https://youtu.be/4JJFrjkRxmo dolphin
def create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('musics:index')
    else:
        form = MusicForm()
    context = {
        'form': form,
    }
    return render(request, 'musics/create.html', context)
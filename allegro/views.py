from django.shortcuts import render
from django.http import HttpResponse
from allegro import image_operation


# Create your views here.

def mozaika(request,*args,**kwargs):
    if "zdjecia" in request.GET:
        #pobranie urli do zdj
        urls = request.GET['zdjecia']

        urls = urls.split(',')
        message = ''

        for  i,url in enumerate(urls):
            #pobieranie zdj
            ok = image_operation.dowland_img(url)
            if ok != 'ok':
                return HttpResponse('dowland error: {} prosze sprawdzic poprawnosc url-a'.format(ok))


        resolution = ''
        #pobranie rozdzielczosci
        if 'rozdzielczosc' in request.GET:
            resolution = request.GET['rozdzielczosc']
        else:
            resolution = '2048x2048'

        #pobieranie wartosci losowo
        random = 'z'
        if 'losowo' in request.GET:
            random = request.GET['losowo']

        # towrzenie moaiki
        ok = image_operation.make_mosaic(resolution,random)

        # sprawdzenie czy mozaika dobrze sie zrobila
        if ok == 'ok':
            return render(request,'allegro/index.html')
        else:
            if ok != 'za duzo url':
                return HttpResponse("blad przy tworzeniu mozaiki error: {} \n prosze sprawdzic czy zostal dobrze podaby url do zdj".format(ok))
            else:
                return HttpResponse("Prosze o podanie mniejszej liczby url-i")

    else:
        return HttpResponse('przsze o wprowadze urli')

def Test(request):
    return render(request,'allegro/testing.html')



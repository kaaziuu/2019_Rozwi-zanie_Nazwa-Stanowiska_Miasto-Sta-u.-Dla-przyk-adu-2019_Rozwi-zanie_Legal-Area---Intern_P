import urllib.request
from PIL import Image

import random
#globalny licznik aby każe nowo pobrane zdj miało inną nazwę
ct = 0
mct = 0

# ta funkcja pobiera zdj z linka url
def dowland_img(url):

    global  ct
    #otworzenie plisku w ktorym beda zapisywane tymczsowe zdj
    path = 'allegro/image/'+str(ct)+'.jpg'
    ct += 1
    file = open(path,'wb')




    #pobranie zdjecia i zapisanie zdjecia
    try:
        headers = {}
        url = url.replace('../','')
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        req = urllib.request.Request(url,headers=headers)
        img = urllib.request.urlopen(req)
        file.write(img.read())
    except Exception as ex:
        ct = 0
        file.close()
        return str(ex)






    file.close()
    return 'ok'

#funkcja tworzżca mozaikę
def make_mosaic(resolution,los):
    global  mct
    global ct

    # proba oczytu rodzelczosci jesli nie jest ustawiona lub zle wpisana
    #ustawiana jest domyslna
    try:
        resolution = resolution.split('x')
        resolution[0] = int(resolution[0])
        resolution[1] = int(resolution[1])
    except:
        resolution = [2048,2048]

    #otworzenie wszystkich wczesniej pobranych zdj
    image_arr = []
    path = 'allegro/image/'
    for i in range(0,ct):

        im = Image.open(path+str(i)+'.jpg')
        image_arr.append(im)

    if len(image_arr) > 8:
        ct = 0
        ret = 'za duzo url'
        return ret

    ct = 0


    #ustalenie wysokosci i szerokosci pojedynczego zdj
    hmuh = len(image_arr)//2

    if len(image_arr) % 2 == 1:
        hmuh += 1

    HI = resolution[1]/hmuh

    WI = resolution[0]/2

    #tworzenie mozaki po przez doklejanie pobranych zdj
    mosaic = Image.new('RGB',(resolution[0],resolution[1]))

    x_offset = 0
    y_offset = 0
    if los != 1 and los != '1':
        # zdjęcia układane po kolei

        for j,img in enumerate(image_arr):

            img = img.resize((int(WI), int(HI)), Image.ANTIALIAS)


            if j == len(image_arr)-1 and j %2 == 0:
                mosaic.paste(img,(x_offset+(int(WI/2)),y_offset))
            else:
                mosaic.paste(img,(x_offset,y_offset))

            if j % 2 ==1:
                x_offset = 0
                y_offset += int(HI)
            else:
                x_offset += int(WI)


    else:
        #losoo dobierane zdj

        len_arr = len(image_arr)
        for i in range(len_arr):
            img = random.choice(image_arr)
            image_arr.remove(img)
            img = img.resize((int(WI), int(HI)), Image.ANTIALIAS)

            if i == len_arr - 1 and i % 2 == 0:
                mosaic.paste(img, (x_offset + (int(WI / 2)), y_offset))
            else:
                mosaic.paste(img, (x_offset, y_offset))

            if i %2 == 1:
                x_offset = 0
                y_offset += int(HI)
            else:
                x_offset += int(WI)




    #zapisanie nowej mozaiki
    mct += 1
    try:
        tmp_img = Image.open('allegro/static/mosaic/new.jpeg')
        tmp_img.save('allegro/static/mosaic/'+str(mct)+'.jpeg')
        mosaic.save('allegro/static/mosaic/new.jpeg')
    except:
        mosaic.save('allegro/static/mosaic/new.jpeg')


    ct = 0
    return 'ok'







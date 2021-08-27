import requests
from bs4 import BeautifulSoup
from random import randint




def getPagesCount():
    pages = []
    resp = requests.get(f'https://anime-pictures.net/pictures/view_posts/0?search_tag=loli&order_by=date&ldate=0&lang=ru')
    soup = BeautifulSoup(resp.text, 'lxml')
    for page_link in soup.find_all('a', class_ = 'disable_on_small'):
        try:
            lpart = page_link.get('href')[1:].split('/')[2]
            pages.append(int(lpart.partition('?')[0]))
        except IndexError:
            pass

    return max(pages)


def randomLoliPicture():
    global count
    count = 0
    for page in range(getPagesCount()):
        ret = []
        resp = requests.get(f'https://anime-pictures.net/pictures/view_posts/{page}?search_tag=loli&order_by=date&ldate=0&lang=ru')
        soup = BeautifulSoup(resp.text, 'lxml')
        for link in soup.find_all('a'):
            tmp = link.get('href')[1:].split('/')
            try:
                if tmp[0] == 'pictures' and tmp[1] == 'view_post':
                    ret.append('/'.join(tmp))
            except IndexError:
                pass
        try:
            link = f'https://anime-pictures.net/{ret[randint(1, len(ret))]}'
            try:
                resp = requests.get(link)
            except:
                raise Exception('Subpage Error')

            soup = BeautifulSoup(resp.text, 'lxml')
            try:
                count+=1
                imgtag = soup.find_all('img', {"id": "big_preview"}).pop()
                imglink = f"http:{imgtag.get('src')}"
                print(count, ")" , imglink)

                filename = imglink.split('/')[-1]
                r = requests.get(imglink, allow_redirects=True)
                open(f"./loli/{filename}", 'wb').write(r.content)

                print("Успешно скачано!")
            except:
                pass
        except:
            pass

print(randomLoliPicture())


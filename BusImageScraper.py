from bs4 import BeautifulSoup
import requests
import re
import shutil

def remove_newlines(data_arr):
    new_data = ""
    for data in data_arr:
        if data != "":
            new_data += data
    
    return new_data

def get_image(url, i):
    url = "https:" + url
    print(url)

    print("Downloading image...")
    r = requests.get(url, stream=True) #Get request on full_urlif r.status_code == 200:                     #200 status code = OK
    with open(f"imgs/img{i}.jpg", 'wb') as f: 
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return

def gallery_request(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    dds = soup.find_all("dd", {"class": "col-9"})
    
    if len(dds) == 0: 
        return False, None, None
    
    service = ""
    for dd in dds:
        div = dd.div
        if div is not None:
            div_text = div.text.split("\n")
            if re.match("^Serviço", div_text[1]):
                service = div_text[2]
    
    if service != "":
        img_url = soup.find_all("img", {"id": "photo"})[0]["src"]
        return True, service, img_url

    return False, None, None

i = 0
csv = open("bus_data.csv", "a")

url = "https://onibusbrasil.com/valtermendonca/page/"

idoridx = 1
while True: 
    print(f"Acessando imagens de {url + str(idoridx)}")
    
    r = requests.get(url + str(idoridx))
    if (r.status_code == 404):
        print(f"{url + str(idoridx)} [404]")
        break

    soup = BeautifulSoup(r.text, "html.parser")

    galleries = soup.find_all("div", {"class": "col-6 col-sm-4 col-md-3 col-xl-2 text-center mb-2"})
    for gallery in galleries:
        gallery_url = gallery.a["href"]
        print("Indo para:", gallery_url)
        hasService, service, img_url = gallery_request(gallery_url)
        if not hasService:
            continue
        
        get_image(img_url, i)
        csv.write(f"{i},{service}\n")
        i += 1

    print(f"Número de Imagens Baixadas: {i + 1}")
    idoridx += 1
import zipfile
from  requests import get
from os import path,system,rmdir,remove
from bs4 import BeautifulSoup
from math import ceil
from time import time
from downloader_maktabkhooneh import progress_bar
from config_info_maktabkhooneh import read_once_run,write_once_run

url_edge = 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
url_chrome = 'https://chromedriver.chromium.org/downloads'
install_webDriver_path = path.dirname(path.abspath("webDriver")).replace('\\','/')+'/webDriver'
chunk_size_byte = 10*1024
name_file = ''


def download_zip(link):
    system('cls')
    print('-'*65,'\n')
    response = get(link, stream=True)
    name_file = link.split('/')[-1]
    print(f"Downloading file: {name_file}")
    path_file = install_webDriver_path + f'/{name_file}'
    current_size_downloaded = 0
    number_chunk =0
    video_size_byte = int(response.headers.get('content-length', 0))
    number_divisions = ceil(video_size_byte/chunk_size_byte)
    with open(f'{path_file}', 'wb') as file_zip:
        progress_bar(0,number_divisions,text=f"\t{0:,.2f} MB downloaded")
        for chunk in response.iter_content(chunk_size_byte):
            number_chunk += 1
            if chunk:
                file_zip.write(chunk)
                current_size_downloaded += len(chunk)
                current_size_downloaded_MB  =current_size_downloaded/(1024*1024)
                progress_bar(number_chunk,number_divisions,text=f"\t{current_size_downloaded_MB:,.2f} MB downloaded")
    print(f"Download completed => {name_file} {current_size_downloaded_MB:,.2f} MB\n")
    print('-'*65,'\n')


def extract_delete_zip():
    with zipfile.ZipFile(install_webDriver_path+'/edgedriver_win64.zip', 'r') as zip_ref:
        zip_ref.extractall(install_webDriver_path)
    if path.exists(install_webDriver_path+'/edgedriver_win64.zip'):
        remove(install_webDriver_path+'/edgedriver_win64.zip')
    else:
        print("The file does not exist")

    system('DEL webDriver\Driver_Notes\credits.html')
    system('DEL webDriver\Driver_Notes\EULA')
    system('DEL webDriver\Driver_Notes\LICENSE')
    rmdir(install_webDriver_path+'/Driver_Notes')


def install_webDriver():
    is_install_webDriver = read_once_run()[0]
    if not eval(is_install_webDriver):
        write_once_run(True,False)
        find_webDriver_edge()
        
# this function not used       
def find_webDriver_chrome():
    response_html = get(url_chrome).text
    soup = BeautifulSoup(response_html,'html.parser')
    div_version = soup.find('div',{'class':'tyJCtd mGzaTb Depvyb baZpAe'})
    a_tags = div_version.find_all('a',{'class':'XqQF9c'},limit=3)
    href_list = []
    for a_tag in a_tags:
        href = a_tag['href']
        print(href)
        href_list.append(href)


def find_webDriver_edge():
    response_html = get(url_edge).text
    soup = BeautifulSoup(response_html,'html.parser')
    div_stabel_driver = soup.find('div',{'class':'bare driver-downloads'})
    a_tags = div_stabel_driver.find_all('a')
    href_list = []
    link_win64 = a_tags[3]['href']
    link_win32 = a_tags[4]['href']
    while True:
        windows = input('choose Win32 or Win64 ?')
        if windows == 'win32':
            start =time()
            download_zip(link_win32)
            end = time()
            print('\ntime download =>',(end-start)/60)
            extract_delete_zip()
            break
        elif windows == 'win64':
            start =time()
            download_zip(link_win64)
            end = time()
            print('time download =>',(end-start)/60)
            extract_delete_zip()
            break
        else:
            print('please Enter win32 or win64 !!')

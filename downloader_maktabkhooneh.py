# from encodings import utf_8
# from selenium.webdriver.common import keys
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import sys, system, path
from time import sleep
from config_info_maktabkhooneh import *
from requests import get
from colorama import Fore
from math import ceil
from find_webDriver import *


def progress_bar(progress, current_size_downloaded, color=Fore.YELLOW, text=''):
    percent = 50 * (progress/float(current_size_downloaded))
    bar = '█' * int(percent) + '-'*(50-int(percent))
    print(color, f'\r|{bar}|{percent*2:.2f}%'+text, end='\r')
    if progress == current_size_downloaded:
        print(Fore.GREEN, f'\r|{bar}|{percent*2:.2f}%'+text, end='\r')
        print('\n\nsuccessful!👌')
        print(Fore.RESET)


def write_video_file(response, number_video):
    str_number = '0' + \
        str(number_video) if len(str(number_video)) == 1 else number_video

    path_file = video_path + f'/session{str_number}'
    current_size_downloaded = 0
    number_chunk = 0
    video_size_byte = int(response.headers.get('content-length', 0))
    print(
        f"Downloading file: session{str_number} {video_size_byte/(1024*1024):.2f} MB ")
    number_divisions = ceil(video_size_byte/chunk_size_byte)
    with open(f'{path_file}.mp4', 'wb') as video_file:
        progress_bar(0, number_divisions, text=f"\t{0:,.2f} MB downloaded")
        for chunk in response.iter_content(chunk_size_byte):
            number_chunk += 1
            if chunk:
                video_file.write(chunk)
                current_size_downloaded += len(chunk)
                current_size_downloaded_MB = current_size_downloaded / \
                    (1024*1024)
                progress_bar(number_chunk, number_divisions,
                             text=f"\t{current_size_downloaded_MB:,.2f}MB downloaded")
                sys.stdout.flush()
    print(
        f"Download completed => session{str_number} {current_size_downloaded_MB:,.2f} MB\n")
    print('-'*65, '\n')


def download_video():
    with open(video_path+'/link_vedios_course.txt', 'r') as link_file:
        link_list = link_file.read().replace("'", '').split('\n')
    print('number video in course: ', len(link_list[:-1]))
    print('-'*65, '\n')
    number = start_video
    for link in link_list[start_video-1:end_video-1]:
        response = get(link, stream=True)
        write_video_file(response, number)
        number += 1


def extract_link_video():
    link_page_video = []
    link_videos = []
    element_video = driver.find_elements(
        by=By.CSS_SELECTOR, value='.js-collapsible__body--active .desktop-unit-nav__unit')
    for element in element_video:
        link_page_video.append(element.get_attribute('href'))
    for page in link_page_video:
        system('cls')
        driver.get(page)
        elem_link_video = driver.find_elements(
            by=By.CSS_SELECTOR, value='.button--round')
        link_videos.append(elem_link_video[0].get_attribute('href'))
    with open(video_path+'/link_vedios_course.txt', 'w') as file:
        for link in link_videos:
            file.write(link+'\n')


def authentication():
    driver.find_element(by=By.CSS_SELECTOR, value='.button').click()
    sleep(2.2)
    username_input = driver.find_element(by=By.CSS_SELECTOR, value='.english')
    username_input.send_keys(phone)
    tags_input = driver.find_elements(
        by=By.TAG_NAME, value='input')
    use_tag = []
    for tag in tags_input:
        if tag.get_attribute('value') == 'ادامه' or \
            tag.get_attribute('name') == 'password' or \
                tag.get_attribute('value') == 'ورود':
            use_tag.append(tag)
    use_tag[0].click()
    sleep(2)
    use_tag[1].send_keys(password)
    sleep(2)
    try:
        use_tag[2].click()
        sleep(3.2)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        sleep(1)
        driver.find_element(
            by=By.XPATH, value='//*[@id="button-visibility"]/a').click()
    except:
        print("Your username or password is incorrect 🤔!!")


if __name__ == '__main__':
    flag_open = True
    if path.exists(install_webDriver_path+'/chromedriver.exe'):
        print('exist webDriver chromedriver.exe')
    elif path.exists(install_webDriver_path+'/msedgedriver.exe'):
        print('exist webDriver Edge')
    else:
        save_info()
        install_webDriver()
    save_info()
    if not exist_link_videos_course:
        if path.exists(install_webDriver_path+'/chromedriver.exe'):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')
                driver = webdriver.Chrome(chrome_driver_path, options=options)
            except:
                flag_open = False
        elif path.exists(install_webDriver_path+'/msedgedriver.exe'):
            try:
                options = webdriver.EdgeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')
                driver = webdriver.Edge(edge_driver_path, options=options)
            except:
                flag_open = False
        else:
            flag_open = False
            print('Driver not found or The version software does not match 🤔!!')
        if flag_open:
            driver.maximize_window()
            driver.get(main_url)
            authentication()
            extract_link_video()
            driver.quit()
    if is_download == 'y':
        download_video()

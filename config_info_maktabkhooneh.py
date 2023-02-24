from os import path

# implement Functions
# ----------------------------


def read_once_run():
    with open('once_run.txt', 'r') as file:
        readed_file = file.read().split('\n')
    save_info = readed_file[1]
    return save_info


def read_info():
    with open('info.txt', 'r')as file:
        readed_file = file.read().split('\n')
    for row in readed_file[1:]:
        info_list = row.split(',')
    phone, password = info_list[0], info_list[1]
    return phone, password


def save_info():
    text_info = f'phone,password\n{phone},{password}'
    with open('info.txt', 'w') as save_file:
        save_file.write(text_info)
    with open('once_run.txt', 'w') as file:
        file.writelines(['saveInfo\n', 'True'])


# ----------------------------
# take your details
if (not path.exists('once_run.txt')):
    with open('once_run.txt', 'w') as file:
        file.writelines(['saveInfo\n', 'False'])
is_save_info = eval(read_once_run())
if not is_save_info:
    phone = input('Please Enter your Phone?')
    password = input('Please Enter your password?')
else:
    phone = read_info()[0]
    password = read_info()[1]
video_path = input('Please Enter path Videos?')
main_url = input('Please Enter Url of your course?')
while True:
    is_download = input('are you want download video?(y/n)')
    if is_download == 'y' or is_download == 'n':
        break
if is_download == 'y':
    while True:
        is_all_video = input('Do you want to download all videos?(y/n)')
        if is_all_video == 'y' or is_all_video == 'n':
            break
    if is_all_video == 'n':
        start_video = int(input('Please Enter number Start video?'))
        end_video = int(input('Please Enter number End video?'))
    else:
        start_video = 1
        end_video = 0
# ----------------------------
# Default program
exist_link_videos_course = path.exists(video_path+'/link_vedios_course.txt')
chunk_size_byte = 1024**2
edge_driver_path = "webDriver\\msedgedriver.exe"
chrome_driver_path = "webDriver\\chromedriver.exe"

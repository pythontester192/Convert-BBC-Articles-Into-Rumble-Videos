from httpcore import TimeoutException
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os, time

f = open('news/news.json')
data = json.load(f)

email = ""
password = ""
rumble_channel = ""

dir_path = '.\\videos'
count = 0
list_videos = []

print("IMPORTANT: Please make sure the name of the videos are like the titles of BBC Article!")
time.sleep(5)

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        for article in data:
            if os.path.basename(path).split(".mp4")[0] == article["title"]:
                vid_path = os.path.abspath("videos/{}".format(str(path)))
                article["video_path"] = vid_path
                list_videos.append(article)
                count += 1
    else:
        print("Error! File Path Not Found.")

if(count == 0):
    print("Error! Couldn't Find Any Video Match BBC Articles.")
if(count > 0):     
    print("   ", count, " Videos found in the videos folder, ready to upload...")
    time.sleep(2)

    options = Options()
    options.add_argument("--lang=en")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.maximize_window()
    browser.get("https://rumble.com")
    time.sleep(3)

    login_button = browser.find_element(By.XPATH, '/html/body/header/div/button[3]').click()
    time.sleep(2)
    email_input = browser.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(email)
    password_input = browser.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(password)
    time.sleep(2)
    login_button = browser.find_element(By.XPATH, '//*[@id="loginForm"]/button[1]').click()
    time.sleep(5)

    for video in list_videos:
        browser.get("https://rumble.com/upload.php")
        time.sleep(5)

        upload_input = browser.find_element(By.XPATH, '//*[@id="Filedata"]').send_keys(video["video_path"])
        time.sleep(2)

        video_title = browser.find_element(By.XPATH, '//*[@id="title"]').send_keys(video["title"])
        time.sleep(2)

        video_description = browser.find_element(By.XPATH, '//*[@id="description"]').send_keys(video["desc"])
        time.sleep(2)

        img_data = requests.get(video["thumbnail"]).content
        with open('image_name.jpg', 'wb') as handler:
            handler.write(img_data)
        video_thumbnail = browser.find_element(By.XPATH, '//*[@id="customThumb"]').send_keys(os.path.abspath("image_name.jpg"))
        time.sleep(2)

        tags = ", ".join(video["tags"])
        video_tags = browser.find_element(By.XPATH, '//*[@id="tags"]').send_keys(tags)
        time.sleep(2)
        
        channel_selector = browser.find_element(By.XPATH, '//*[@id="channelId"]').click()
        channel_name = browser.find_element(By.XPATH, '//*[@id="channelId"]/option[text()="{}"]'.format(str(rumble_channel))).click()
        time.sleep(2)

        try:
            element = WebDriverWait(browser, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="form"]/div/div[1]/div[1]/div[2]/h2[contains(text(),"100%")]'))
            )
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
        
        upload_button = browser.find_element(By.XPATH, '//*[@id="submitForm"]').click()
        time.sleep(5)

        license_option = browser.find_element(By.XPATH, '//*[@id="form2"]/div/div[2]/div[2]/div/a').click()
        time.sleep(2)

        condition_checkbox1 = browser.find_element(By.XPATH, '//*[@id="form2"]/div/div[7]/div[1]/label').click()
        condition_checkbox2 = browser.find_element(By.XPATH, '//*[@id="form2"]/div/div[7]/div[2]/label').click()
        time.sleep(2)
        
        submit_button = browser.find_element(By.XPATH, '//*[@id="submitForm2"]').click()
        time.sleep(20)
        
print("The Bot Finished Uploading Rumble Videos!")
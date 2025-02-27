from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
import subprocess
import speech_recognition as sr
def captcha_resolve(driver,Invisible,delay):
    recognizer = sr.Recognizer()
    if Invisible == False:
        try:
            WebDriverWait(driver, delay).until(EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span#recaptcha-anchor"))).click()
        except:
            return 0
    driver.switch_to.default_content()
    try:
        WebDriverWait(driver, delay).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")))
    except:
        return 0
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-play-button button")))
    src = driver.find_element(By.ID,"audio-source").get_attribute("src")
    local_mp3_file = "downloaded_audio.mp3"
    try:
        response = requests.get(src)
        response.raise_for_status()
        with open(local_mp3_file, "wb") as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"{e}")
        exit()
    subprocess.call(['ffmpeg', '-y','-i', 'downloaded_audio.mp3',
                    'downloaded_audio.wav'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                    )
    local_wav_file = 'downloaded_audio.wav'
    try:
        with sr.AudioFile(local_wav_file,) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(text)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#audio-response"))).send_keys(text)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".verify-button-holder button"))).click()
    except Exception as e:
        print(f"Error as {e}")
    return driver

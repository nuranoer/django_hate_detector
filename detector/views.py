from django.shortcuts import render
from django.http import JsonResponse
from textblob import TextBlob
from nrclex import NRCLex
import nltk
import tweepy

import os
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
from langdetect import detect
from textblob.translate import NotTranslated
import time 


nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')



def detect_emotion_sentiment(tweet):
# Deteksi bahasa tweet
    tweet_language = detect(tweet)

    if tweet_language != 'en':
        # Jika bahasa bukan bahasa Inggris, maka terjemahkan
        try:
            obj = TextBlob(tweet)
            translated_tweet = obj.translate(from_lang=tweet_language, to='en')
        except NotTranslated:
            # Jika tidak dapat diterjemahkan, gunakan teks asli
            translated_tweet = TextBlob(tweet)
    else:
        # Jika sudah dalam bahasa Inggris, gunakan langsung
        translated_tweet = TextBlob(tweet)  
          
    # Deteksi emosi
    emotion = NRCLex(str(translated_tweet))
    detected_emotion = emotion.top_emotions
    
    # Deteksi sentimen
    sentiment = translated_tweet.sentiment.polarity
    if sentiment == 0:
        detected_sentiment = 'Neutral'
    elif sentiment > 0:
        detected_sentiment = 'Positive'
    else:
        detected_sentiment = 'Negative'
    
    return detected_emotion, detected_sentiment

def post_tweet_to_twitter(twitter_username, twitter_password, tweet):
    try:
        driver=webdriver.Firefox()
        driver.implicitly_wait(10)
         
        driver.maximize_window()

        # Buka halaman login Twitter
        driver.get("https://twitter.com/home")

        # Temukan elemen username
        username_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username_field.send_keys(twitter_username)
        time.sleep(10)

        # Temukan tombol "Next"
        next_btn = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        next_btn.click()
        time.sleep(2)

        # Temukan elemen password
        password_field = driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")
        password_field.send_keys(twitter_password)
        time.sleep(2)

        # Temukan tombol "Login"
        login_btn = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div')
        login_btn.click()
        time.sleep(2)

        # Temukan elemen textarea untuk menulis tweet
        tweet_area = driver.find_element(By.XPATH,"//*[@contenteditable='true']")
        tweet_area.send_keys(tweet)
        time.sleep(2)

        # Temukan tombol "Tweet"
        tweet_button = driver.find_element(By.XPATH,"//div[@data-testid='tweetButtonInline']")
        tweet_button.click()
        time.sleep(5)

    except Exception as e:
        print(e)
    
    finally:
        # Tutup WebDriver
        driver.quit()
        
def post_to_twitter(request):
    if request.method == 'POST':
        twitter_username = request.POST.get('twitter_username')
        twitter_password = request.POST.get('twitter_password')
        tweet = request.POST.get('tweet')

        try:
            post_tweet_to_twitter(twitter_username, twitter_password, tweet)
            response_data = {'success': True, 'message': 'Tweet posted successfully!'}
        except Exception as e:
            response_data = {'success': False, 'message': f'Error: {str(e)}'}

        return JsonResponse(response_data)
    
    return render(request, 'home')

def home(request):
    detected_emotion = None
    detected_sentiment = None
    tweet = None

    if request.method == 'POST':
        tweet = request.POST.get('tweet')
        if tweet:
            detected_emotion, detected_sentiment = detect_emotion_sentiment(tweet)
    
    context = {
        'tweet': tweet,
        'detected_emotion': detected_emotion,
        'detected_sentiment': detected_sentiment,
    }

    return render(request, 'home.html', context)

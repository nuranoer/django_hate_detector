from django.shortcuts import render
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
import time 


nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

def detect_emotion_sentiment(tweet):
    obj = TextBlob(tweet)
    translated_tweet = obj.translate(from_lang='id', to='en')
    
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

def twitter_login(username, password):
    driver = webdriver.Firefox()
    try:
        twitter_home_page = 'https://twitter.com/login'
        driver.get(twitter_home_page)
        driver.implicitly_wait(3)
        driver.maximize_window()

        username_elem = driver.find_element(By.XPATH, "//input[@name='session[username_or_email]']")
        username_elem.send_keys(username)

        password_elem = driver.find_element(By.XPATH, "//input[@name='session[password]']")
        password_elem.send_keys(password)

        login_btn = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
        login_btn.click()

        time.sleep(4)

    except Exception as e:
        print(e)

    return driver

def send_tweet(driver, tweet_text):
    try:
        sendmessage = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        sendmessage.send_keys(tweet_text)
        time.sleep(2)

        kliktweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
        kliktweet.click()
        time.sleep(5)
    except Exception as e:
        print(e)

def post_to_twitter(request):
    if request.method == 'POST':
        tweet = request.POST.get('tweet')
        if tweet:
            username = '@izzapsdkukediri'  # Replace with your Twitter username
            password = 'abidatulizzah90*'  # Replace with your Twitter password
            driver = twitter_login(username, password)
            send_tweet(driver, tweet)
            driver.quit()

    return render(request, 'home.html')

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

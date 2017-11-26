import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from stransfer import stranfer
import json
import pytest


@pytest.fixture()
def driver():
    chop = webdriver.ChromeOptions()
    chop.add_argument("--no-sandbox")
    chop.add_argument("--no-default-browser-check")
    chop.add_argument("--no-first-run")
    chop.add_argument("--disable-default-apps")
    driver = webdriver.Chrome(chrome_options=chop)
    yield driver
    driver.quit()


def test_transfer_from_requests_to_selenium_login_http(driver):
    s = requests.Session()
    url = 'http://testing-ground.scraping.pro/login?mode=login'
    s.post(url, data={'usr': 'admin', 'pwd': '12345'})
    stranfer(s, driver, url)
    driver.get('http://testing-ground.scraping.pro/login?mode=welcome')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    expect_welcome_text = soup.select_one('div#case_login').text.strip()
    assert 'WELCOME ' in expect_welcome_text


def test_transfer_from_requests_to_selenium_cookie_https(driver):
    s = requests.Session()
    driver.get('https://httpbin.org/cookies')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pre = soup.select_one('pre').text
    pre_ret = json.loads(pre)

    url = 'https://httpbin.org/cookies/set?name=stransfer&value=42'
    s.get(url)
    stranfer(s, driver, url)
    driver.get('https://httpbin.org/cookies')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pre = soup.select_one('pre').text
    post_ret = json.loads(pre)
    assert (pre_ret['cookies'] == {} and
            post_ret['cookies']['name'] == 'stransfer' and
            post_ret['cookies']['value'] == '42')


def test_transfer_from_selnium_to_requests_login_http(driver):
    s = requests.Session()
    url = 'http://testing-ground.scraping.pro/login'
    driver.get(url)
    # login
    driver.find_element_by_css_selector('input#usr').send_keys('admin')
    driver.find_element_by_css_selector('input#pwd').send_keys('12345')
    driver.find_element_by_css_selector('input#pwd').submit()
    stranfer(driver, s, url)
    r = s.get('http://testing-ground.scraping.pro/login?mode=welcome')
    soup = BeautifulSoup(r.text, 'html.parser')
    expect_welcome_text = soup.select_one('div#case_login').text.strip()
    assert 'WELCOME ' in expect_welcome_text


def test_transfer_from_selenium_to_requests_cookie_https(driver):
    s = requests.Session()
    r = s.get('https://httpbin.org/cookies')
    pre_ret = r.json()
    url = 'https://httpbin.org/cookies/set?name=stransfer&value=42'
    driver.get(url)
    stranfer(driver, s, url)
    r = s.get('https://httpbin.org/cookies')
    post_ret = r.json()
    assert (pre_ret['cookies'] == {} and
            post_ret['cookies']['name'] == 'stransfer' and
            post_ret['cookies']['value'] == '42')


def test_transfer_wrong_source_target_two_sessions():
    s = requests.Session()
    t = requests.Session()
    s.get('https://httpbin.org/cookies')
    url = 'https://httpbin.org/cookies/set?name=stransfer&value=42'
    with pytest.raises(TypeError):
        stranfer(s, t, url)


def test_transfer_wrong_source_target_two_chromes():
    with pytest.raises(TypeError):
        stranfer('foo', 'bar', 'http://example.com')

'''
import os
os.system("pip install selenium==3.141.0")
os.system('pip install pandas')
os.system('pip install beautifulsoup4')
'''
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

search = "http://www.icargo.net/icargo/do/searchFlight"
edge_options = Options()
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=edge_options)
driver.get(search)
deplist = []
arrlist = []
time_format = '%H:%M'
username = 'sqarrdep@gmail.com'
password = 'txtx dwgh yovt goth'
mail_from = 'sqarrdep@gmail.com'

mail_to = [
    'szeleon_tee@sats.com.sg', 'sekar_nagaraj01@sats.com.sg',
    'kevin_castillo@sats.com.sg', 'jefferson_torres@sats.com.sg',
    'sri_rao@sats.com.sg', 'gilberto_david@sats.com.sg',
    'muhammadaliff_ahmad@sats.com.sg'
]

arr_flights = [
    '517', '535', '523', '441', '537', '103', '949', '991', '131', '105', 
    '107', '153', '725', '935', '133', '615', '147', '163', '727', '761',
    '113', '171', '155', '525', '115', '252', '509', '117', '137', '165',
    '173', '431', '735', '157', '929', '995', '906', '141', '193', '204', 
    '739', '135', '981', '927', '723', '731', '901', '519', '183' 
]

dep_flights = [
    '934', '104', '154', '524', '990', '762', '132', '726', '251', '203',
    '164', '148', '508', '172', '106', '108', '134', '728', '432', '156',
    '906', '114', '166', '174', '194', '116', '138', '118', '736', '158',
    '928', '740', '442', '142', '994', '522', '516', '534', '948', '536', 
    '616', '136', '980', '926', '724', '900', '728', '184' 
]


def get_current_time(f='%Y-%b-%d %H:%M'):
  format_time = datetime.datetime.now() + datetime.timedelta(hours=8)
  current_time = format_time.strftime('%H:%M')
  current_day = format_time.strftime('%d')
  current_month = format_time.strftime('%b')
  return current_time, current_day, current_month


def convert_list(data):
  df = pd.DataFrame(data)
  df[['Flight', 'No.', 'STD', 'Time', 'Bay']] = df[0].str.split(' ',
                                                                expand=True)
  df.drop(columns=0, inplace=True)
  df['Time'] = pd.to_datetime(df['Time'], format=time_format)
  df['Time'] = df['Time'].apply(lambda row: row.strftime(time_format))
  df = df.sort_values(by='Time', ascending=True)
  df['string'] = df.apply(lambda row: ' '.join(row), axis=1)
  df.drop(columns=['Flight', 'No.', 'STD', 'Time', 'Bay'], inplace=True)
  lst = df['string'].tolist()
  return lst


def dep_list():
  for i in dep_flights:
    try:
      time_, day_, mth_ = get_current_time()
      driver.get(search)
      input_box_1 = driver.find_element(
          By.XPATH,
          '//td[@class="crtCellText"]/input[@class="crtCellMan" and @name="flightNo1" and @value=""]'
      )
      input_box_2 = driver.find_element(
          By.XPATH,
          '//td[@class="crtCellText"]/input[@class="crtCellMan" and @name="flightNo2" and @value=""]'
      )
      input_box_1.click()
      input_box_1.send_keys('SQ')
      input_box_2.click()
      input_box_2.send_keys(i)
      input_box_2.send_keys(Keys.ENTER)
      html_source = driver.page_source
      soup = BeautifulSoup(html_source, "html.parser")

      if i == '906':
        flight_status = soup.find_all('td', class_='bdCellText')[22]
        flight_bay = soup.find_all('td', class_='bdCellText')[33]
        aircraft_type = soup.find_all('td', class_='bdCellText')[31]
      else:
        flight_status = soup.find_all('td', class_='bdCellText')[4]
        flight_bay = soup.find_all('td', class_='bdCellText')[17]
        aircraft_type = soup.find_all('td', class_='bdCellText')[13]

      flight_status = flight_status.text.strip()
      flight_status = flight_status.replace(f'{day_} {mth_} 2023 /', '')
      flight_bay = flight_bay.text.strip()
      result = f'SQ {i} STD{flight_status} {flight_bay}'

      types = ['B738', 'B38M']
      aircraft_type = aircraft_type.text.strip()
      if any(aircraft_type == types for types in types):
        deplist.append(result)
        sleep(1)
    except Exception:
      pass


def arr_list():
  for i in arr_flights:
    try:
      time_, day_, mth_ = get_current_time()
      driver.get(search)
      input_box_1 = driver.find_element(
          By.XPATH,
          '//td[@class="crtCellText"]/input[@class="crtCellMan" and @name="flightNo1" and @value=""]'
      )
      input_box_2 = driver.find_element(
          By.XPATH,
          '//td[@class="crtCellText"]/input[@class="crtCellMan" and @name="flightNo2" and @value=""]'
      )
      input_box_1.click()
      input_box_1.send_keys('SQ')
      input_box_2.click()
      input_box_2.send_keys(i)
      input_box_2.send_keys(Keys.ENTER)
      html_source = driver.page_source
      soup = BeautifulSoup(html_source, "html.parser")

      if i == '906':
        aircraft_type = soup.find_all('td', class_='bdCellText')[31]
      else:
        aircraft_type = soup.find_all('td', class_='bdCellText')[13]

      flight_status = soup.find_all('td', class_='bdCellText')[4]
      flight_status = flight_status.text.strip()
      flight_status = flight_status.replace(f'{day_} {mth_} 2023 /', '')
      flight_bay = soup.find_all('td', class_='bdCellText')[17]
      flight_bay = flight_bay.text.strip()
      result = f'SQ {i} STA{flight_status} {flight_bay}'

      types = ['B738', 'B38M']
      aircraft_type = aircraft_type.text.strip()
      if any(aircraft_type == types for types in types):
        arrlist.append(result)
        sleep(1)
    except Exception:
      pass


def dep_mail_list():
  mail_subject = f'DEP FLIGHTS'
  dep_list_msg = '\n'.join(deplist)
  mail_body = dep_list_msg
  msg = MIMEMultipart()
  msg['From'] = username
  msg['To'] = ', '.join(mail_to)
  msg['Subject'] = mail_subject
  msg.attach(MIMEText(mail_body, 'plain'))
  text = msg.as_string()
  connection = smtplib.SMTP('smtp.gmail.com')
  connection.starttls()
  connection.login(username, password)
  connection.sendmail(mail_from, mail_to, text)
  connection.quit()


def arr_mail_list():
  mail_subject = f'ARR FLIGHTS'
  arr_list_msg = '\n'.join(arrlist)
  mail_body = arr_list_msg
  msg = MIMEMultipart()
  msg['From'] = username
  msg['To'] = ', '.join(mail_to)
  msg['Subject'] = mail_subject
  msg.attach(MIMEText(mail_body, 'plain'))
  text = msg.as_string()
  connection = smtplib.SMTP('smtp.gmail.com')
  connection.starttls()
  connection.login(username, password)
  connection.sendmail(mail_from, mail_to, text)
  connection.quit()


if __name__ == '__main__':
  while True:
    try:
      dep_list()
      deplist = convert_list(data=deplist)
      print(deplist)
      dep_mail_list()
      arr_list()
      arrlist = convert_list(data=arrlist)
      print(arrlist)
      arr_mail_list()
      print(deplist)
      deplist.clear()
      arrlist.clear()
      sleep(3600)
    except Exception as e:
      print(e)
      pass

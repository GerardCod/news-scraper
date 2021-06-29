import requests
import lxml.html as html
import os 
import datetime

HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class ="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

def parse_home():
  try:
    response = requests.get(HOME_URL)
    
    if response.status_code == 200:
      home = response.content.decode('utf-8')
      parsed = html.fromstring(home)
      link_to_new = parsed.xpath(XPATH_LINK_TO_ARTICLE)
      today = datetime.date.today().strftime("%d-%m-%Y")
      dirname = f'gaguilar-{today}'
      if not os.path.isdir(dirname):
        os.mkdir(dirname)
        print(f'Directorio {dirname} creado exitosamente')

      for link in link_to_new:
        parse_notice(link, dirname)
    else:
      raise ValueError(f'Error: {response.status_code}')
  
  except ValueError as error:
    print(error)


def parse_notice(link, today):
  try:
    response = requests.get(link)
    if response.status_code == 200:
      notice = response.content.decode('utf-8')
      parsed = html.fromstring(notice)

      try:
        title = parsed.xpath(XPATH_TITLE)[0]
        title = title.replace('\"', '')
        title = title.replace('\'', '')
        title = title.replace('“', '')
        summary = parsed.xpath(XPATH_SUMMARY)[0]
        body = parsed.xpath(XPATH_BODY)
      except IndexError:
        return

      with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as file:
        file.write(title)
        file.write('\n\n')
        file.write(summary)
        file.write('\n\n')
        for p in body:
          file.write(p)
          file.write('\n\n')
      print(f'Archivo {title}.txt creado exitosamente')
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve)


def run():
  parse_home()

if __name__ == '__main__':
  run()
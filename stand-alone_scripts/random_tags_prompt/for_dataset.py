import requests
from bs4 import BeautifulSoup
import sys
import random
import shutil
from time import sleep
import cloudscraper
from tqdm import tqdm


ALL_THE_TAGS = True

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


def danbooru_dataset(url='https://danbooru.donmai.us/posts/random', tags_all=True, additional_tags= ''):

  scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'firefox', 'platform': 'linux',})
  req = scraper.get(url)
  text = req.content
  
  
  
  # r = requests.get(url, headers=headers, allow_redirects=True)


  soup = BeautifulSoup(text,'html.parser')
  tab = soup.find("div",{"class":"tag-list categorized-tag-list"})

  tables = tab.findAll('ul')

  tag_dict = {table.get('class')[0]:table for table in tab.findAll('ul')}
  # "tag-type-0" - general-tag-list
  # "tag-type-1" - artist-tag-list
  # "tag-type-3" - copyright-tag-list
  # "tag-type-4" - character-tag-list
  # "tag-type-5" - meta-tag-list

  tag_types = [['general-tag-list', "tag-type-0"],
    ['artist-tag-list', "tag-type-1"], None,
    ['copyright-tag-list', "tag-type-3"],
    ['character-tag-list', "tag-type-4"],
    ['meta-tag-list', "tag-type-5"]]

  if tags_all:
    tag_types_idx = [0, 1 , 3, 4]
  else:
    tag_types_idx = [0]

  all_the_tags = []

  for tag_idx in tag_types_idx:
      try:
          tag_slice = tag_dict[tag_types[tag_idx][0]]
          all_the_tags.append([_['data-tag-name'] for _ in tag_slice.findAll('li')])
      except Exception as e:
          print('ERROR:', e)

  all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
  all_the_tags = all_the_tags.replace('_', ' ')
  all_the_tags = all_the_tags.replace('(', '\(').replace(')', '\)')


  img_link = text.decode('utf-8').split('Size: <a href="')
  img_link = img_link[1].split('">')
  img_link = img_link[0]

  file_name = img_link.split('/')[-1]

  res = requests.get(img_link, stream = True, headers=headers, allow_redirects=True)

  if res.status_code == 200:
      with open(file_name,'wb') as f:
          shutil.copyfileobj(res.raw, f)
      print('Image sucessfully Downloaded: ',file_name)
  else:
      print('Image Couldn\'t be retrieved')


  all_the_tags = additional_tags + ' ' + all_the_tags

  text_file_name = file_name.split('.')[0] + '.txt'
  with open(text_file_name, 'w', encoding='utf-8') as f:
    f.write(all_the_tags)



def gelbooru_dataset(url='https://gelbooru.com/index.php?page=post&s=random', tags_all=True, additional_tags= ''):
    r = requests.get(url, headers=headers, allow_redirects=True)
    r.text

    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("ul",{"class":"tag-list"})

    tag_types =['tag-type-artist',
    'tag-type-character',
    'tag-type-copyright',
    'tag-type-metadata',
    'tag-type-general']

    if tags_all:
      tag_types_idx = [0, 1 , 4]
    else:
      tag_types_idx = [-1]



    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        try:
            tag_type = tag_types[tag_type_idx]
            tags = [_ for _ in tab.findAll('li') if _.get("class") == [tag_type]]
            all_the_tags.append([[_.text for _ in tag.findAll('a')][-1] for tag in tags])
        except Exception as e:
            print('ERROR:', e)
    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    all_the_tags = all_the_tags.replace('(', '\(').replace(')', '\)')


    img_link = r.text.split('class="fit-width" src="')[1].split('">')[0]

    file_name = img_link.split('/')[-1]

    res = requests.get(img_link, stream = True, headers=headers, allow_redirects=True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')


    all_the_tags = additional_tags + ' ' + all_the_tags

    text_file_name = file_name.split('.')[0] + '.txt'
    with open(text_file_name, 'w', encoding='utf-8') as f:
      f.write(all_the_tags)


def safebooru_dataset(url='https://safebooru.org/index.php?page=post&s=random', tags_all=True, additional_tags= ''):
    r = requests.get(url, headers=headers, allow_redirects=True)


    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("ul",{"id":"tag-sidebar"})


    tag_types = ['tag-type-copyright tag',
    'tag-type-character tag',
    'tag-type-artist tag',
    'tag-type-general tag',
    'tag-type-metadata tag']
    tag_types = [_.split(' ') for _ in tag_types]

    if tags_all:
      tag_types_idx = [0, 1, 2, 3]
    else:
      tag_types_idx = [-2]



    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        try:
            tag_type = tag_types[tag_type_idx]
            tags = [_ for _ in tab.findAll('li') if _.get('class') == tag_types[tag_type_idx]]
            all_the_tags.append([[_.text for _ in tag.findAll('a')][-1] for tag in tags])
        except Exception as e:
            print('ERROR:', e)

    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    all_the_tags = all_the_tags.replace('(', '\(').replace(')', '\)')


    img_link = r.text.split('" id="image" onclick="if ')[0].split('" src=')[-1].split(" id=")[0].replace('"', '').split('?')[0]

    file_name = img_link.split('/')[-1]

    res = requests.get(img_link, stream = True, headers=headers, allow_redirects=True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')


    all_the_tags = additional_tags + ' ' + all_the_tags

    text_file_name = file_name.split('.')[0] + '.txt'
    with open(text_file_name, 'w', encoding='utf-8') as f:
      f.write(all_the_tags)

def e621_dataset(url='https://e621.net/popular', tags_all=True, additional_tags= ''): 
    r = requests.get(url, headers=headers, allow_redirects=True)


    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("section",{"id":"tag-list"})


    tag_types =['artist-tag-list',
                'species-tag-list',
                'general-tag-list',
                'meta-tag-list']


    if tags_all:
      tag_types_idx = [0, 1, 2]
    else:
      tag_types_idx = [1, 2]


    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        try:
            tag_type = tag_types[tag_type_idx]
            tags = [_ for _ in tab.findAll('ul') if _.get("class") == [tag_types[tag_type_idx]]]
            tags =  [_.text for _ in tags[0].findAll('a') if _.get("class") == ['search-tag']] 
            all_the_tags.append([tags])
        except Exception as e:
            print('ERROR:', e)


    flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
    all_the_tags = flatten(all_the_tags)



    all_the_tags = ', '.join( all_the_tags)
    all_the_tags = all_the_tags.replace('_', ' ')
    all_the_tags = all_the_tags.replace('(', '\(').replace(')', '\)')

    img_link = r.text.split('<meta property="og:image" content="')[1].split('">')[0]

    file_name = img_link.split('/')[-1]

    res = requests.get(img_link, stream = True, headers=headers, allow_redirects=True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')


    all_the_tags = additional_tags + ' ' + all_the_tags

    text_file_name = file_name.split('.')[0] + '.txt'
    with open(text_file_name, 'w', encoding='utf-8') as f:
      f.write(all_the_tags)




def e926_dataset(url='https://e926.net/popular', tags_all=True, additional_tags= ''): 
    r = requests.get(url, headers=headers, allow_redirects=True)


    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("section",{"id":"tag-list"})


    tag_types =['artist-tag-list',
                'species-tag-list',
                'general-tag-list',
                'meta-tag-list']


    if tags_all:
      tag_types_idx = [0, 1, 2]
    else:
      tag_types_idx = [1, 2]


    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        try:
            tag_type = tag_types[tag_type_idx]
            tags = [_ for _ in tab.findAll('ul') if _.get("class") == [tag_types[tag_type_idx]]]
            tags =  [_.text for _ in tags[0].findAll('a') if _.get("class") == ['search-tag']] 
            all_the_tags.append([tags])
        except Exception as e:
            print('ERROR:', e)


    flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
    all_the_tags = flatten(all_the_tags)



    all_the_tags = ', '.join( all_the_tags)
    all_the_tags = all_the_tags.replace('_', ' ')
    all_the_tags = all_the_tags.replace('(', '\(').replace(')', '\)')

    img_link = r.text.split('<meta property="og:image" content="')[1].split('">')[0]

    file_name = img_link.split('/')[-1]

    res = requests.get(img_link, stream = True, headers=headers, allow_redirects=True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')


    all_the_tags = additional_tags + ' ' + all_the_tags

    text_file_name = file_name.split('.')[0] + '.txt'
    with open(text_file_name, 'w', encoding='utf-8') as f:
      f.write(all_the_tags)





def download_from_source(source, url, additional_tags=''):
    if 'gelbooru' in source:
      gelbooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    elif 'danbooru' in source:
      danbooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    elif 'safebooru' in source:
      safebooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    elif 'e621' in source:
      e621_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    elif 'e926' in source:
      e926_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    else:
      assert False, "You can only use links from gelbooru, danbooru and safebooru"


argv = sys.argv


if sys.argv[1] != 'txt':
    url = sys.argv[1]
    source = url.split('.')[0]
    additional_tags = ' '.join(argv[2:])
    try:
        download_from_source(source, url, additional_tags)
    except Exception as e:
        print('ERROR', e, url)
        
    # if 'gelbooru' in source:
      # gelbooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    # elif 'danbooru' in source:
      # danbooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    # elif 'safebooru' in source:
      # safebooru_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    # elif 'e621' in source:
      # e621_dataset(url=url, tags_all=ALL_THE_TAGS, additional_tags=additional_tags)
    # else:
      # assert False, "You can only use links from gelbooru, danbooru and safebooru"

elif sys.argv[1] == 'txt':
    fname = sys.argv[2]
    with open(fname, 'r') as f:
        data = f.readlines()
    for url in tqdm(data):
        try:
            url = url.strip()
            source = url.split('.')[0]
            download_from_source(source, url)
            sleep(1)
        except Exception as e:
            print('ERROR', e, url)
            

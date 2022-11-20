from operator import itemgetter
import random
import sys


with open('danbooru.csv', 'r', encoding='utf-8') as f:
    data = f.readlines()

data = [_.strip() for _ in data]
data = [_.split(',') for _ in data]
data = sorted(data, key=lambda x:int(x[2]))[::-1]
data = [[_[1:3], [_[0]] + _[3:]] for _ in data]


stop = 15000 # in order to cut very rare ones
data_caped = data[:stop]
data_caped = [_ for _ in data_caped if _[0][0] == '0']
random.sample(data_caped, 20)


try: # use "python random_tags_prompt.py NUMBER_OF_TAGS" 
    length = int(sys.argv[1])
except: # or just put the number in here
    length = 15

data_caped_proc = [_[1] for _ in data_caped]
prompt = random.sample(data_caped_proc, length)
prompt = [[__ for __ in _ if __] for _ in prompt]
prompt = [random.sample(_,1)[0] for _ in prompt]
prompt = ', '.join(random.sample(prompt, length))
prompt = prompt.replace('"', '')
prompt = prompt.replace('_',' ')
prompt = prompt.replace('(','\\(')
prompt = prompt.replace(')','\\)')
print(prompt)

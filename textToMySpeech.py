# -*- coding: utf-8 -*-
#IMPORT all the packages
pip install pydub

from bs4 import BeautifulSoup
from IPython.display import Audio
from google.colab import drive
import re
import requests
import wave as wv 
from pydub import AudioSegment

#Setup the file system with a connection to google drive. Here are your phonetic files located
drive.mount('/content/drive/', force_remount=True)

def play(file):
  return Audio(file, autoplay=True)

#The phonetic functions
listWoordAf = []

def getFonetic(word):
  toReturn = ''

  with requests.Session() as s:    
    url = 'https://nl.wiktionary.org/wiki/{}'.format(word)
    r = s.get(url)
    if 'Deze pagina bevat geen tekst' in r.text:
      word = word.capitalize()
      url = 'https://nl.wiktionary.org/wiki/{}'.format(word)
      r = s.get(url)
    
    soup = BeautifulSoup(r.text, 'html')
    if "Woorden in het Nederlands met IPA-weergave" not in soup.text:
      ipa = False    
    else:
      ipa = soup.find('a', text='IPA')
      
    if ipa:
      ipa = ipa.parent()[1].text.replace('/', '').replace('\u202f', '')
      ipa = ipa.split('\n')[0].replace('(Noord-Nederland): ', '').split(',')[0]
      toReturn = list(ipa)
      woordAf = soup.find('span', {'class' : 'mw-headline', 'id' : 'Woordafbreking'}).parent.find_next_sibling()
      woordAf = woordAf.text.split('·')
      if woordAf:
        listWoordAf.append(woordAf)
      else:
        listWoordAf.append(word)
    
    else:
      woordAf = soup.find('span', {'class' : 'mw-headline', 'id' : 'Woordafbreking'})
      
      if woordAf:
        woordAf = woordAf.parent.find_next_sibling()
        woordAf = woordAf.text.split('·')
        listWoordAf.append(woordAf)
      else:
        listWoordAf.append(word)
      word = word.lower()
      url = 'http://www.woorden.org/woord/{}'.format(word)
      r = s.get(url)
      soup = BeautifulSoup(r.text, 'html')
      if len(soup.find_all('table')) != 0:
          table = soup.find_all('table')[0]
          if len(table.find_all('td')) > 0:
            tData = table.find_all('td')[1].text
            tData = tData.replace('[', '').replace(']', '')
            toReturn = list(tData)
          else: 
            print("Dit woord is onbekend:", word)
            toReturn = list(word)
      else:
        print("Dit woord is onbekend:", word)
        toReturn = list(word)

  if 'ː' in toReturn:
    index = toReturn.index('ː')
    toReturn[(index - 1):(index+1)] = [''.join(toReturn[(index -1 ):(index+1)])]
  
  if ':' in toReturn:
    index = toReturn.index(':')
    toReturn[(index - 1):(index+1)] = [''.join(toReturn[(index -1 ):(index+1)])]
  if '(' in toReturn:
    toReturn.remove('(')
    toReturn.remove(')')
    #     index = toReturn.index('(')
    #     toReturn[(index):(index+3)] = [''.join(toReturn[(index):(index+3)])]

  if 'ˈ' in toReturn:
    toReturn.remove('ˈ')
    #index = toReturn.index('ˈ')
    #toReturn[(index):(index+2)] = [''.join(toReturn[(index):(index+2)])] 
  if "'" in toReturn:
    toReturn.remove("'")
    #index = toReturn.index("'")
    #toReturn[(index):(index+2)] = [''.join(toReturn[(index):(index+2)])]
    
  return toReturn

def toFonArray(string):
  fonArray = []
  string = string.replace(' ', ' &nbsp; ').replace(' .', '&#46;').replace(' ,', '&#44;').lower()
  array = string.split(' ')
  for word in array:
    if word == '&#44;' :
      fonArray.append('comma')
    elif word == '&#46;' :
      fonArray.append('do')
    elif word == '&nbsp;' :
      fonArray.append('space')
    else:
      word = word.lower()
      fonArray.append(getFonetic(word))
  
  return fonArray

ipaSampa = {"χ" : "x", "a":"adp","e":"edp","ɪː":"idp", "o": "odp","p":"p", "t":"t", "k":"k", "f":"f", "s":"s", "ʃ":"ss", "x":"x", "b":"b", "d":"d", "ɡ":"g", "v":"v", "z":"z", "ʒ":"zz", "ɣ":"gg", "ɦ":"h_", "l":"l", "r":"r", "m":"m", "n":"n", "ŋ":"nn", "j":"j", "w": "v_", "ʋ":"v_", "tʃ":"tS", "ts":"ts", "dʒ":"dZ", "ɑ":"aa", "ɛ":"eedp", "ɪ":"ii", "ɔ":"oo", "ʏ":"yy", "ə":"@", "aː":"adp","eː":"edp", "i":"i", "oː":"odp", "y":"y", "øː":"2dp", "u":"u", "ɛː":"eedp", "œː":"9dp","iː":"idp", "yː":"ydp", "ɔː":"oodp", "uː":"udp", "ɛi":"Ei", "œy":"9y", "ʌu":"Vu", "ɑi":"Ai", "ɔi":"i", "aːi":"adpi", "eːu":"edpu", "iu":"iu", "oːi":"odpi", "ui":"ui"}

def toAudio(lijst):
  audioList = []
  outFileTo = '/content/drive/My Drive/speech/results/{}.wav'.format(file_name)
  outfilePlay = '/content/drive/My Drive/speech/results/{}.wav'.format(file_name)

  for fonWord in lijst:
    if type(fonWord) is str:
      fonWord = '{}.wav'.format(fonWord)
      audioList.append(fonWord)
    elif type(fonWord) is list:
      for ch in fonWord:
        if ch == "ø":
          ch = "øː"
        if ch in ipaSampa:
          ch = ipaSampa[ch]
          print('character ', ch, 'in ipaSampa')
        else:
          ch = ch
          print('character ', ch, 'not in ipaSampa')
        ch =  '{}.wav'.format(ch)
        audioList.append(ch)
      
  data= []
  
  begEind = AudioSegment.from_wav("/content/drive/My Drive/speech/first.wav")
  fileEx = begEind
  for file in audioList:
    file = '/content/drive/My Drive/speech/{}'.format(file)
    song = AudioSegment.from_wav(file)
    fileEx = fileEx.append(song, crossfade=10)
  
  fileEx = fileEx.append(begEind, crossfade=100)
  fileEx.export(outFileTo, format="wav")
  
  print('DONE')
  return True

ipaSampa = {"ɱ":"mm","ɲ":"ng", "a":"adp","e":"edp","ɪː":"idp", "o": "odp","p":"p", "t":"t", "k":"k", "f":"f", "s":"s", "ʃ":"ss", "x":"x", "b":"b", "d":"d", "ɡ":"g", "v":"v", "z":"z", "ʒ":"zz", "ɣ":"gg", "ɦ":"h_", "l":"l", "r":"r", "m":"m", "n":"n", "ŋ":"nn", "j":"j", "ʋ":"v_", "tʃ":"tS", "ts":"ts", "dʒ":"dZ", "ɑ":"aa", "ɛ":"eedp", "ɪ":"ii", "ɔ":"oo", "ʏ":"yy", "ə":"@", "aː":"adp","eː":"edp", "i":"i", "oː":"odp", "y":"y", "øː":"2dp", "u":"u", "ɛː":"eedp", "œː":"9dp","iː":"idp", "yː":"ydp", "ɔː":"oodp", "uː":"udp", "ɛi":"Ei", "œy":"9y", "ʌu":"Vu", "ɑi":"Ai", "ɔi":"i", "aːi":"adpi", "eːu":"edpu", "iu":"iu", "oːi":"odpi", "ui":"ui"}


# Result
#@title Form {vertical-output: true }
#@markdown After pressing ctrl+enter there will be an audiofile created
listWoordAf = []
text = 'The text to my speech' #@param {type:"string"}
file_name = 'myFirstSpeech' #@param {type:"string"}

forAudio = toFonArray(text)

TF = toAudio(forAudio)
  
play('/content/drive/My Drive/spraak/results/{}.wav'.format(file_naam))

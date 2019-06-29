# TextToMySpeech
With this python programm, you can put in your own speech fonetics to make a text-to-speech with your own voice!

## setup
First of all you will have to record all of the phonetic sounds of your language one by one. Each .wav file of a phonetic sound must correspond to exactly one phonetic character. The better you record the phonetic sounds, the better your text to speech will work. To record these sounds, say a word which contains a phonetic character you need to record, and then isolate that sound. Then save it with the SAMPA naming. Most file systems dont see the difference between a capital letter and a normal one so use for a capital Z in sampa zz.wav.

For the English use the following wikipedia article:

[https://en.wikipedia.org/wiki/SAMPA_chart_for_English](https://en.wikipedia.org/wiki/SAMPA_chart_for_English)

For Dutch, use this one:

[https://nl.wikipedia.org/wiki/Klankinventaris_van_het_Nederlands](https://nl.wikipedia.org/wiki/Klankinventaris_van_het_Nederlands)

If you know more, please feel free to add more languages

## Explanation of the functions
### play(Audio file)
``` py
def play(file):
```
A Function to quickly play an audio file

### getFonetic(String)
``` py
def getFonetic(word):
```
This function returns a list with the phonetic characters in IPA of a given word.
This funciton only searches the dutch wikitonary and an other dutch words website. If you arent Dutch, you use for example: en.wikitionary.org

### toFonArray(String)
``` py
def toFonArray(string)
```
This function replaces most of the punctuation marks in a given string, sentence or a whole paragraph.
Also it puts the words in the getFonetic function one by one, and in the end, it returns all the phonetic characters in a list

###  toAudio(List with Phonetics)
``` py
def toAudio(lijst)
```
This function converts a list of phonetic characters to an audio file. And that file gets uploaded to your google drive

### ipaSampa
``` py
ipaSampa = {"ɱ":"mm","ɲ":"ng", "a":"adp","e":"edp","ɪː":"idp", "o": "odp","p":"p", "t":"t", "k":"k", "f":"f", "s":"s", "ʃ":"ss", "x":"x", "b":"b", "d":"d", "ɡ":"g", "v":"v", "z":"z", "ʒ":"zz", "ɣ":"gg", "ɦ":"h_", "l":"l", "r":"r", "m":"m", "n":"n", "ŋ":"nn", "j":"j", "ʋ":"v_", "tʃ":"tS", "ts":"ts", "dʒ":"dZ", "ɑ":"aa", "ɛ":"eedp", "ɪ":"ii", "ɔ":"oo", "ʏ":"yy", "ə":"@", "aː":"adp","eː":"edp", "i":"i", "oː":"odp", "y":"y", "øː":"2dp", "u":"u", "ɛː":"eedp", "œː":"9dp","iː":"idp", "yː":"ydp", "ɔː":"oodp", "uː":"udp", "ɛi":"Ei", "œy":"9y", "ʌu":"Vu", "ɑi":"Ai", "ɔi":"i", "aːi":"adpi", "eːu":"edpu", "iu":"iu", "oːi":"odpi", "ui":"ui"}
```
Here you have to put the phonetics of your language, see wikipedia or wikitionary for you language. 
I use the SAMPA format for the phonetic files. Thus in this list i convert the ipa format from wikitionary or woorden.org to the SAMPA format

It works like this:
``` py
ipaSampa["ɱ"] #a string in IPA formate
>>>mm #the corresponding string in SAMPA format
```


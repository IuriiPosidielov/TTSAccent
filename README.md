# TTSAccent

Written for personal use to generate fairy tales for child

App main features;
  - makes accents in format silero '+' symbol 
  - divide text on bunches to avoid silero text limitation
  - generate for each bunch tts and then join to one result file
  - if still some mistakes in accents can be fixed using userDictionary
  
Requirement (dependencies):
   - model.ts - silero model for tts
   - rudict.db - database with accents from Vuizur https://github.com/Vuizur/add-stress-to-epub/releases/download/v1.0.1/russian_dict.zip 
  
How use:
    1. put text in input.txt
    2. run python3 main.py
    3. generated file sounds.wav - contains tts with accents

import io
import os
import torch
from pydub.playback import play
from pydub import AudioSegment
import time
from accent.rutextStresser import rutextStresser
import time
import wave

# cleanup old request
import os, shutil
folder = './temp'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

if os.path.isfile("sounds.wav"):
    os.unlink("sounds.wav")


userDictionary = {"Королева": '.Королева', ".королева": 'королева', 'замок': 'з+амок'}

def nearestDelimiter(txt,  cur):
    try:
        delimiters = ".!?"          
        if(txt[cur] in delimiters) :          
            return cur
        else:
            i=cur
            while ( i>=0 ):
                if (txt[i] in delimiters) :                    
                            return i
                i=i-1
        return 0
    except Exception as e:
         return 0
    

def splitTextMultiple(sentence,chunkLength):
     cursor = 0  
     curlng = chunkLength
     lst = []
     while (curlng < len(sentence)):
         curlng = nearestDelimiter(sentence, curlng)       
         substr = (sentence[cursor : curlng]).strip()
         cursor = curlng        
         curlng = (cursor+chunkLength*3) if (cursor+chunkLength<len(sentence)) else len(sentence)
         if not substr: break
         lst.append(substr)
     print("subfinish " + sentence[cursor : curlng])            
     laststr =  (sentence[cursor : curlng]).strip()
     if laststr:   
        lst.append(laststr)
     return lst

def silero_voice(txt, i):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    sample_rate = 48000 #24000
    speaker = 'xenia'

    audio_paths = model.save_wav(text=txt, speaker=speaker, sample_rate=sample_rate, put_accent=True, put_yo=False)
    audio_file = AudioSegment.from_wav(audio_paths)
    
start_time = time.time()

# read text from file
pathToFile = "D:\python\Python\python\silero\input.txt"
with open(pathToFile, encoding = 'utf-8', mode = 'r') as f:
    content = f.read()

# extra fix all not standard stress words
userDictionaryLen = len(userDictionary)
for key in userDictionary:
    content = content.replace(key, userDictionary[key])
print("extra fix:")
print(content)


# stress text using big stress dictionary
ts = rutextStresser()

s = ts.stress_text(content)
# make stress in tts format
res = ""
for element in range(0, len(s)-1):
    if ord(s[element]) == 769: continue
    if ord(s[element+1]) == 769:
        res = res + "+" + s[element]
    else:
        res = res + s[element]

res = res + s[len(s)-1]
print(res)

# post fix
res = res.replace("корол+ева?", "Королева.")
# split text on chunks as tts limitation
list = splitTextMultiple(res, 300)

# generate wav for every chunk
i = 0
chunkLength = len(list)
for element in range(0, chunkLength):
    i = i + 1
    print(list[element])
    silero_voice(list[element], element)
    time.sleep(1)
    s = str(i)
    fl = "temp/temp" + s + ".wav"
    os.rename("test.wav", fl)
    
print("Silero: --- %s seconds ---" % (time.time() - start_time))

# join wav chunks in single file
infiles = []
for i in range(1, chunkLength+1):
    infiles.append("temp/temp" + str(i) + ".wav")

outfile = "sounds.wav"

data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
    
output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()
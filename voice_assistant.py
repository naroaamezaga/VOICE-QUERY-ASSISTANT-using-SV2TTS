# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:22:22 2021

@author: naroa
"""
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

import os
from sys import exit
from datetime import datetime

import sqlite3
import csv

import sounddevice as sd
import soundfile as sf

import warnings


# changing directory for importing SV2TTS implementation
os.chdir(os.path.abspath(os.path.dirname("Real-Time-Voice-Cloning/")))


from IPython.utils import io
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa

# ignore warnings
warnings.filterwarnings("ignore")

 
# initializing all the encoder libraries           
encoder_weights = Path("encoder/saved_models/pretrained.pt")
vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
syn_dir = Path("synthesizer/saved_models/logs-pretrained/taco_pretrained")
encoder.load_model(encoder_weights)
synthesizer = Synthesizer(syn_dir)
vocoder.load_model(vocoder_weights)

# changing directory for importing welcoming audio
os.chdir(os.path.abspath(os.path.dirname("../../../intro_error_messages/intros/")))

# play welcoming message 
print("\n\033[0;30;47mWELCOME TO YOUR VIRTUAL ASSISTANT, HOW CAN I HELP YOU?\n")
sound = AudioSegment.from_wav('intro_naroa_original.wav')
play(sound)

# changing directory for saving recorded questions
os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname("Questions/")))

# create the recognizer
r = sr.Recognizer()

# define the microphone
'''print(sr.Microphone.list_microphone_names())
print(sr.Microphone.list_microphone_names()[0])'''
mic = sr.Microphone(device_index=0)

# record speech from microphone
with mic as source:
    
    # adjust parameters
    r.adjust_for_ambient_noise(source,duration=1)
    r.energy_threshold = 1000
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_adjustment_ratio = 1.5
    r.pause_threshold = 3
    
    print("\033[0;30;47mAsk your question please.\n")
    print("\033[0;30;47mRecording audio...\n")
    
    # listen to the question from microphone
    audio = r.listen(source,timeout=5)
    
    print("\033[0;30;47mAudio recording finished!\n")
    
    # save question in a .wav file naming it with date and time
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y(%H-%M-%S)")
    filename="question_"+timestampStr+".wav"
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    f.close()
    
    '''# play saved question audio
    sound = AudioSegment.from_wav(filename)
    play(sound)'''
    
    try:
        
        # convert audio into text
        print("\033[0;30;47mConverting audio into text...\n")
            
        # GOOGLE SPEECH RECOGNITION
        result = r.recognize_google(audio,language="en-US") # English
        print("\033[0;30;47mText: "+result+"\n")
        result=result.lower()
      
        # CMU SPHINX
        '''result = r.recognize_sphinx(audio,language="en-US")
        print("\033[0;30;47mText: "+result+"\n")'''
        
        print("\033[0;30;47mAudio converted into text!\n")
            
    except Exception as e:

        print ("\033[0;30;47mCould not convert audio. Try again. \n")
        print (e)

# get keywords from question
word_list = []
    
for words in result.split(' '):
    if (words == 'the') or (words =='is') or (words =='for') or (words == 'in') or (words == 'are') or (words == 'course') or (words == 'professor\'s') or (words == 'professors') or (words == 'office') or (words == 'room') or (words == 'penalty') or (words == 'submission') or (words == 'required') or (words == 'exam') or (words =='is') or (words == 'which') or (words == 'what') or (words == '?'):
        continue
    else:
        word_list.append(words)
        
print("\033[0;30;47mThe keywords are: ")
print(word_list)

# prepare sql query string
sqlquery = []
sqlquery.append("SELECT ")

when = False
array = False
count = None
name = word_list.copy()

for loop in word_list:

    if loop == ('when') or loop == ('When'):
        when = True
        name.remove(loop)
    elif loop == ('telephone'):
        sqlquery.append("telephone FROM ")
        name.remove(loop)
    elif loop == ('email'):
        sqlquery.append("email FROM ")
        name.remove(loop)
    elif loop == ('address'):
        sqlquery.append("office FROM ")
        name.remove(loop)
    elif loop == ('hours'):
        sqlquery.append("office_hours FROM ")
        name.remove(loop)
    elif loop == ('schedule'):
        sqlquery.append("lectures FROM ")
        name.remove(loop)
    elif loop == ('textbook'):
        sqlquery.append("textbook FROM ")
        name.remove(loop)
    elif loop == ('attendance'):
        sqlquery.append("attendance FROM ")
        name.remove(loop)
    elif loop == ('assignment'):
        sqlquery.append("assig")
        name.remove(loop)
    elif loop == ('presentation'):
        sqlquery.append("present")
        name.remove(loop)
    elif loop == ('midterm'):
        sqlquery.append("midterm")
        name.remove(loop)
        if when == True:
            sqlquery.append("_date FROM ")
    elif loop == ('final'):
        sqlquery.append("final")
        name.remove(loop)
        if when == True:
            sqlquery.append("_date FROM ")
    elif loop == ('due') or loop == ('do'):
        sqlquery.append("_dates FROM ")
        name.remove(loop)
        array = True
    elif loop == ('grading'):
        sqlquery.append("_grade FROM ")
        name.remove(loop)
    elif loop == ('late'):
        sqlquery.append("late_submission FROM ")
        name.remove(loop)
    elif loop == ('first') or loop == ('one') or loop == ('1'):
        count = '1' 
        name.remove(loop)
    elif loop == ('second') or loop == ('two') or loop == ('2'):
        count = '2'
        name.remove(loop)
    elif loop == ('third') or loop == ('three') or loop == ('3'):
        count = '3'
        name.remove(loop)
    elif loop == ('fourth') or loop == ('four') or loop == ('4'):
        count = '4'
        name.remove(loop)
    elif loop == ('fifth') or loop == ('five') or loop == ('5'):
        count = '5'
        name.remove(loop)


course_name = ' '.join(name)
if course_name == 'human-computer interaction':
    course_name = 'human computer interaction'
elif course_name == 'internet technology and web design':
    course_name == 'internet technologies and web design'
sqlquery.append("courses_table WHERE course_name=")
sqlquery.append("'"+course_name+"'")
strsqlquery= ''.join(sqlquery) + ';'

print("\n\033[0;30;47mThe SQL query is: ")
print(strsqlquery)

# database connection
conn = None
try: 
    # in-memory database
    conn = sqlite3.connect(":memory:")
    
except Exception as e:
 
    print("\033[0;30;47mCannot connect to database")
    print(e)

print("\n\033[0;30;47mDatabase cuccessfully connected to SQLite")

# create table
cur = conn.cursor()
cur.execute("CREATE TABLE courses_table (course_code,course_name,semester,year,first_name,last_name,telephone,email,office,office_hours,lectures,textbook,attendance,assig_dates,present_dates,midterm_date,final_date,assig_grade,present_grade,midterm_grade,final_grade,late_submission);") 

with open('../../../course_db/courses_table.csv','r') as courses_table:
    dr = csv.DictReader(courses_table) # comma is default delimiter
    to_db = [(i['course_code'], i['course_name'], i['semester'], i['year'], i['first_name'], i['last_name'], i['telephone'], i['email'], i['office'], i['office_hours'], i['lectures'], i['textbook'], i['attendance'], i['assig_dates'], i['present_dates'], i['midterm_date'], i['final_date'], i['assig_grade'], i['present_grade'], i['midterm_grade'], i['final_grade'], i['late_submission']) for i in dr]

cur.executemany("INSERT INTO courses_table VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
conn.commit()

# execute sql query
cur.execute(strsqlquery)

# get answer
answer = cur.fetchone()
print(answer)

# build whole answer sentence
word_list = []
textbook = False
    
for words in result.split(' '):
    if (words == 'what') or (words =='when') or (words == 'which') or (words == 'required') or (words == '?'):
        continue 
    elif (words == 'is'):
        verb = ' is '
    elif (words == 'are'):
        verb = ' are '
    elif (words == 'due') or (words == 'do'):
        verb = ' is due '
    else:
        word_list.append(words)

sentence = " ".join(word_list)     

try:
    for words in answer[0].split(' '):
        if(words == 'No'):
            textbook = True
        
    if textbook == True:
        sentence = 'There'

    if count is not None:
        if answer[0][0:5]=='There':
            ans=answer[0][0:-1].split(', ')
            ans=ans+" in this course"
            print("\n\033[0;30;47mThe answer is: ")
            print(ans)
        else:
            dates = answer[0][1:-1].split(', ')
            if int(count)<=len(dates):
                index = int(count)-1
                final_answer = dates[index]
                str =  ''.join(final_answer[1:-1])
                print("\n\033[0;30;47mThe answer is: ")
                print(str)
                ans = sentence+verb+str
                print(sentence+verb+str)
            else:
                ans="There is no such assignment or presentation in this course" 
                print("\n\033[0;30;47mThere is no such assignment or presentation in this course")            
    elif array is False:
        if answer[0][0:5]=='There':
            ans=answer[0][0:-1].split(', ')
            ans=ans+" in this course"
            print("\n\033[0;30;47mThe answer is: ")
            print(ans)
        else:
            str =  ''.join(answer)
            print("\n\033[0;30;47mThe answer is: ")
            print(str)
            if str[-1]=='%':
                ans = sentence+verb+str[0:2]+' percent.'
                print(ans)
            elif textbook == True:
                ans=sentence+verb+str+" in this course"
                print(ans)
            else:    
                ans = sentence+verb+str
                print(ans)
    else:
        ans="Cannot find the answer to your question"
        print("\n\033[0;30;47mCannot find the answer to your question")
        exit()
except:
    ans="Cannot find the answer to your question" 
    print("\n\033[0;30;47mCannot find the answer to your question") 
    exit()

# get course code
sqlquery = []
sqlquery.append("SELECT course_code FROM courses_table WHERE course_name=")
sqlquery.append("'"+course_name+"'")
strsqlquery= ''.join(sqlquery) + ';'
cur = conn.cursor()
cur.execute(strsqlquery)
course_code = cur.fetchone()

# close database connection
conn.close();

# SV2TTS. CONVERSION INTO AUDIO WITH VOICE CLONING

# get text for converting into audio with cloned voice
text = ans

print("\nStarting conversion into audio with cloned voice (it may take a few minutes)...")

# choose video with cloning voice
minutes="5"
code =  ''.join(course_code)
path="../../VideosAudios/"+code+"/"+code+"_"+minutes+"min_audio.wav"
in_fpath = Path(path)

# change directory for saving voice embeding
os.chdir(os.path.abspath(os.path.dirname("../Cloned_voices_embedings/")))

# save voice embeding if it does not already exist
try:
    embed = np.load(code+'_'+minutes+'min'+'.npy')
    print("\n\033[0;30;47mVoice embeding loaded")
except IOError:
    # change directory for using SV2TTS implementation
    os.chdir(os.path.abspath(os.path.dirname("../Real-Time-Voice-Cloning/")))
    # build voice embeding
    reprocessed_wav = encoder.preprocess_wav(in_fpath)
    original_wav, sampling_rate = librosa.load(in_fpath)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    # change directory for saving voice embeding
    os.chdir(os.path.abspath(os.path.dirname("../Cloned_voices_embedings/")))
    print("\n\033[0;30;47mSaving voice embeding...")
    # save voice embeding
    np.save(code+'_'+minutes+'min', embed)  
    print("\n\033[0;30;47mVoice embeding saved")

# change directory for using SV2TTS implementation
os.chdir(os.path.abspath(os.path.dirname("../Real-Time-Voice-Cloning/")))

# build answer audio with cloned voice
with io.capture_output() as captured:
  specs = synthesizer.synthesize_spectrograms([text], [embed])
generated_wav = vocoder.infer_waveform(specs[0])
generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

# play answer audio with cloned voice
sd.play(generated_wav,synthesizer.sample_rate)

# change directory for saving answer audio with cloned voice
os.chdir(os.path.abspath(os.path.dirname("../Cloned_answers/")))

# save answer audio with cloned voice
sf.write(code+'_cloned_'+minutes+'min_demo'+'.wav',generated_wav,synthesizer.sample_rate)

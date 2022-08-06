# VOICE-QUERY-ASSISTANT-with-SV2TTS

View the research project at: 
https://hawkiit-my.sharepoint.com/:b:/g/personal/namezagavelez_hawk_iit_edu/ESZjIbAbKLJIqv__yoWvuEMBGvOi6roKnkQzNmQElKWNLg?e=ANuZWS

Voice query assistant to request and receive information about a course, such as, professor's contact information, course schedule, exam and assignment dates and grading, etc. It also includes a voice cloning feature that allows to reproduce the answer of the query with the corresponding professor's voice. This is done using the SV2TTS tool by Corentin Jemine (https://github.com/CorentinJ/Real-Time-Voice-Cloning). 

To this end, we have created a syllabus template (docx), which will be converted into a database (csv). This will be done using "converter.py". We have also created a 15 question bank (available in "15_question_bank.pdf" in "Example" directory). 

Then, in order to execute "voice_assistant.py" follow the next steps:


**1. Install Requirements**

Python 3.7 is needed to run the tool.

To install Speech Recognition:
- pip install SpeechRecognition
- pip install pydub
- pip install pyaudio

To install SV2TTS:  
- Clone repository: git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.git   
- Select directory: cd Real-Time-Voice-Cloning/   
- Install Pytorch: pip install torch torchvision    
- Install requirement and dependencies: pip install -r requirements.txt  
- Download pretrained data: gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc
- Unzip: unzip pretrained.zip  

Move these files into Real-Time-Voice-Cloning/

**2. Code configuration** 

Some configurations are needed in the code:  
- Line 346: The parameter "minutes" represents the duration of the reference voice sample that wants to be used to clone the voice. Choose between: 5,15,30,45,60.  
- Line 389: Choose filename where the generated cloned answer will be saved.

**3. Launch Voice Query assistant**

- py voice_assistant.py    

The user will ask one of the possible fifteen questions and this will be captures by the microphone. After performing the SQL query, the answer will be reproduced with the corresponding professor's cloned voice.

**4. Test similarity with Resemblyzer**

The Python package Resemblyzer allows to compare and analyze the cloned voices and the real ones. It provides several demos explained at: https://github.com/resemble-ai/Resemblyzer. To install it:
- git clone https://github.com/resemble-ai/Resemblyzer.git
- pip install resemblyzer


In the "Example" directory, we have included an example implementation of the designed tool. "15_question_bank.pdf" shows the general questions and the specific 15 questions that have been asked to this particular professor about his course named "Advanced Informatics". His original voice and cloned voice (answering to the 15 questions) are included in the zip file.  

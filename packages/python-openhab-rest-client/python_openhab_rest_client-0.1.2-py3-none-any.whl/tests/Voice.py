import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient
from openhab.tests import VoiceTest


if __name__ == "__main__":
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    voiceTest = VoiceTest(client)
    
    text = "Hello from OpenHAB!"
    language = "en"
    sourceID = "enhancedjavasound"
    keyword = "openHAB"
    sttID = "voicerss:enUS"
    ttsID = "voicerss:deDE"
    voiceID = "voicerss:enUS_Mary"
    sinkID = "enhancedjavasound"
    hliIDs = ["rulehli", "system"]
    listeningItem = "testSwitch"
    interpreterID = "system"
    
    voices = voiceTest.testGetVoices()                                                                      # Test #1
    voiceTest.testGetDefaultVoice()                                                                         # Test #2
    if voices:
        voiceTest.testSayText(text, voices[0]["id"], sinkID)                                                # Test #3
    else:
        print("No voices, test skipped.")
    interpreters = voiceTest.testGetInterpreters(language)                                                  # Test #4
    if interpreters:
        voiceTest.testInterpretText(text, language)                                                         # Test #5
    else:
        print("No interpreter, test skipped.")
    if interpreters:
        voiceTest.testInterpretTextBatch(text, [interp["id"] for interp in interpreters[:2]], language)     # Test #6
    else:
        print("No interpreter, test skipped.")
    voiceTest.testGetInterpreter(interpreterID, language)                                                   # Test #7
    voiceTest.testStartDialog(sourceID, keyword, sttID, ttsID, voiceID, sinkID)                             # Test #8
    voiceTest.testStopDialog(sourceID)                                                                      # Test #9
    voiceTest.testListenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem)           # Test #10

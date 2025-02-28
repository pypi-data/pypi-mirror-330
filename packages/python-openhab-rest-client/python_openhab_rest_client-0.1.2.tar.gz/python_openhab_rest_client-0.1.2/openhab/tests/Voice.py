import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Voice

class VoiceTest:
    def __init__(self, client: OpenHABClient):
        self.voiceAPI = Voice(client)

    def testGetDefaultVoice(self):
        print("\n~~~~ Test #1: getDefaultVoice() ~~~~\n")

        try:
            defaultVoice = self.voiceAPI.getDefaultVoice()
            print(f"Default Voice: {defaultVoice}")
        except Exception as e:
            print(f"Error retrieving default voice: {e}")

    def testGetVoices(self):
        print("\n~~~~ Test #2: getVoices() ~~~~\n")

        try:
            voices = self.voiceAPI.getVoices()
            print(json.dumps(voices, indent=4))
            return voices
        except Exception as e:
            print(f"Error retrieving voices: {e}")
            return []

    def testSayText(self, text: str, voiceID: str, sinkID: str, volume: str = '100'):
        print("\n~~~~ Test #3: sayText(text, voiceID, sinkID, volume) ~~~~\n")

        try:
            response = self.voiceAPI.sayText(text, voiceID, sinkID, volume)
            print(f"Text spoken using Voice {voiceID}: {response}")
        except Exception as e:
            print(f"Error speaking text: {e}")

    def testGetInterpreters(self, language: str = None):
        print("\n~~~~ Test #4: getInterpreters(language) ~~~~\n")

        try:
            interpreters = self.voiceAPI.getInterpreters(language)
            print(json.dumps(interpreters, indent=4))
            return interpreters
        except Exception as e:
            print(f"Error retrieving interpreters: {e}")
            return []

    def testInterpretText(self, text: str, language: str = None):
        print("\n~~~~ Test #5: interpretText(text, language, IDs) ~~~~\n")

        try:
            result = self.voiceAPI.interpretText(text, language)
            print(f"Interpreted Text: {result}")
        except Exception as e:
            print(f"Error interpreting text: {e}")

    def testInterpretTextBatch(self, text: str, IDs: list, language: str):
        print("\n~~~~ Test #6: interpretTextBatch(text, language, IDs) ~~~~\n")

        try:
            result = self.voiceAPI.interpretTextBatch(text, IDs, language)
            print(f"Batch Interpreted Text: {result}")
        except Exception as e:
            print(f"Error batch interpreting text: {e}")

    def testGetInterpreter(self, interpreterID: str, language: str = None):
        print("\n~~~~ Test #7: getInterpreter(interpreterID, language) ~~~~\n")

        try:
            interpreter = self.voiceAPI.getInterpreter(interpreterID, language)
            print(f"Interpreter Details: {json.dumps(interpreter, indent=4)}")
        except Exception as e:
            print(f"Error retrieving interpreter: {e}")

    def testStartDialog(self, sourceID: str, keyword: str = None, sttID: str = None, ttsID: str = None, voiceID: str = None, sinkID: str = None, language: str = None):
        print("\n~~~~ Test #8: startDialog(sourceID, keyword, sttID, ttsID, voiceID, sinkID) ~~~~\n")

        try:
            response = self.voiceAPI.startDialog(sourceID=sourceID, keyword=keyword, 
                                                sttID=sttID, ttsID=ttsID, voiceID=voiceID, sinkID=sinkID, language=language)
            if isinstance(response, dict) and "error" in response:
                print(f"Error: {response['error']}")
            else:
                print(f"Dialog started: {json.dumps(response, indent=4)}")
        except Exception as e:
            print(f"Error starting dialog: {e}")


    def testStopDialog(self, sourceID: str):
        print("\n~~~~ Test #9: stopDialog(sourceID) ~~~~\n")

        try:
            response = self.voiceAPI.stopDialog(sourceID)
            print(f"Dialog stopped: {json.dumps(response, indent=4)}")
        except Exception as e:
            print(f"Error stopping dialog: {e}")

    def testListenAndAnswer(self, sourceID: str, sttID: str, ttsID: str, voiceID: str, hliIDs: list, sinkID: str, listeningItem: str):
        print("\n~~~~ Test #10: listenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem) ~~~~\n")

        try:
            response = self.voiceAPI.listenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem)
            print(f"Listen and Answer Response: {json.dumps(response, indent=4)}")
        except Exception as e:
            print(f"Error with Listen and Answer: {e}")

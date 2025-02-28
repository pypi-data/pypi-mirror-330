from .Client import OpenHABClient
import json
import requests


class Voice:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Voice class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getDefaultVoice(self):
        """
        Gets the default voice.

        :return: A dictionary with the details of the default voice.
        """
        try:
            response = self.client.get(
                '/voice/defaultvoice', header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "No default voice was found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No default voice was found."}

        return {"error": f"Unexpected response: {status_code}"}

    def startDialog(self, sourceID: str, ksID: str = None, sttID: str = None,
                    ttsID: str = None, voiceID: str = None, hliIDs: str = None,
                    sinkID: str = None, keyword: str = None, listeningItem: str = None, language: str = None):
        """
        Start dialog processing for a given audio source.

        :param sourceID: The ID of the audio source.
        :param ksID: The ID of the keyword spotter (optional).
        :param sttID: The ID of the speech-to-text system (optional).
        :param ttsID: The ID of the text-to-speech system (optional).
        :param voiceID: The ID of the voice (optional).
        :param hliIDs: A comma-separated list of interpreter IDs (optional).
        :param sinkID: The ID of the audio output (optional).
        :param keyword: The keyword used to start the dialog (optional).
        :param listeningItem: The name of the item to listen to (optional).
        :param language: The language for the request (optional).

        :return: The response from the server.
        """
        header = None
        if language:
            header = {"Accept-Language": language}

        try:
            response = self.client.post('/voice/dialog/start', params={'sourceId': sourceID, 'ksId': ksID, 'sttId': sttID, 'ttsId': ttsID,
                                                                       'voiceId': voiceID, 'hliIds': hliIDs, 'sinkId': sinkID, 'keyword': keyword, 'listeningItem': listeningItem}, header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Services are missing or language is not supported by services or dialog processing is already started for the audio source."}
            #elif status_code == 404:
            #    return {"error": "One of the given ids is wrong."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        #elif status_code == 404:
        #    return {"error": "One of the given ids is wrong."}
        elif status_code == 400:
            return {"error": "Services are missing or language is not supported by services or dialog processing is already started for the audio source."}

        return {"error": f"Unexpected response: {status_code}"}

    def stopDialog(self, sourceID: str):
        """
        Stop dialog processing for a given audio source.

        :param sourceID: The ID of the audio source.
        :return: The response from the server.
        """
        try:
            response = self.client.post(
                '/voice/dialog/stop', params={'sourceId': sourceID})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "No dialog processing is started for the audio source."}
            elif status_code == 404:
                return {"error": "No audio source was found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No audio source was found."}
        elif status_code == 400:
            return {"error": "No dialog processing is started for the audio source."}

        return {"error": f"Unexpected response: {status_code}"}

    def getInterpreters(self, language: str = None):
        """
        Get the list of all interpreters.

        :param language: The language for the request (optional).

        :return: A list of interpreters if successful.
        """
        header = {"Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get('/voice/interpreters', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def interpretText(self, text: str, language: str = None):
        """
        Sends a text to the default human language interpreter.

        :param text: The text to be interpreted.
        :param language: The language of the text.
        :param IDs: A list of interpreter IDs (optional).

        :return: The response from the server.
        """
        header = {"Content-Type": "text/plain", "Accept": "text/plain"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post('/voice/interpreters', header=header, data=text)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Interpretation exception occurs."}
            elif status_code == 404:
                return {"error": "No human language interpreter was found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No human language interpreter was found."}
        elif status_code == 400:
            return {"error": "Interpretation exception occurs."}

        return {"error": f"Unexpected response: {status_code}"}

    def getInterpreter(self, interpreterID: str, language: str = None):
        """
        Gets a single interpreter.

        :param interpreterID: The ID of the interpreter.
        :param language: The language for the request (optional).

        :return: The details of the interpreter.
        """
        header = {"Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f'/voice/interpreters/{interpreterID}', header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Interpreter not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Interpreter not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def interpretTextBatch(self, text: str, IDs: list, language: str = None):
        """
        Sends a text to a given human language interpreter(s).

        :param text: The text to be interpreted.
        :param language: The language of the text.
        :param IDs: A list of interpreter IDs.

        :return: The response from the server.
        """
        header = {"Content-Type": "text/plain", "Accept": "text/plain"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.post('/voice/interpreters', header=header, params={
                                        'ids': ','.join(IDs)}, data=text)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Interpretation exception occurs."}
            elif status_code == 404:
                return {"error": "No human language interpreter was found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No human language interpreter was found."}
        elif status_code == 400:
            return {"error": "Interpretation exception occurs."}

        return {"error": f"Unexpected response: {status_code}"}

    def listenAndAnswer(self, sourceID: str, sttID: str, ttsID: str, voiceID: str,
                        hliIDs: list, sinkID: str, listeningItem: str, language: str = None):
        """
        Executes a simple dialog sequence without keyword spotting for a given audio source.

        :param sourceID: The ID of the audio source.
        :param sttID: The ID of the speech-to-text system.
        :param ttsID: The ID of the text-to-speech system.
        :param voiceID: The ID of the voice.
        :param hliIDs: A list of interpreter IDs (optional).
        :param sinkID: The ID of the audio output (optional).
        :param listeningItem: The name of the item to listen to (optional).
        :param language: The language for the request (optional).

        :return: The response from the server.
        """
        header = None
        if language:
            header = {"Accept-Language": language}

        try:
            response = self.client.post('/voice/listenandanswer', params={'sourceId': sourceID, 'sttId': sttID, 'ttsId': ttsID, 'voiceId': voiceID, 'hliIds': ','.join(
                hliIDs) if hliIDs else None, 'sinkId': sinkID, 'listeningItem': listeningItem}, header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Services are missing or language is not supported by services or dialog processing is already started for the audio source."}
            elif status_code == 404:
                return {"error": "One of the given ids is wrong."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "One of the given ids is wrong."}
        elif status_code == 400:
            return {"error": "Services are missing or language is not supported by services or dialog processing is already started for the audio source."}

        return {"error": f"Unexpected response: {status_code}"}

    def sayText(self, text: str, voiceID: str, sinkID: str, volume: str = '100'):
        """
        Speaks a given text with a given voice through the given audio sink.

        :param text: The text to be spoken.
        :param voiceID: The ID of the voice.
        :param sinkID: The ID of the audio output.
        :param volume: The volume level (default: 100).

        :return: The response from the server.
        """
        try:
            response = self.client.post('/voice/say', params={'voiceId': voiceID, 'sinkId': sinkID, 'volume': volume}, data={
                                        'text': text}, header={"Content-Type": "text/plain"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def getVoices(self):
        """
        Get the list of all voices.

        :return: A list of voices if successful.
        """
        try:
            response = self.client.get(
                '/voice/voices', header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

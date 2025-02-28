from .Client import OpenHABClient
import json
import requests


class Rules:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Rules class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getRules(self, prefix=None, tags=None, summary=False, staticDataOnly=False):
        """
        Get available rules, optionally filtered by tags and/or prefix.

        :param prefix: Optional prefix to filter the results.
        :param tags: Optional tag array to filter the results.
        :param summary: If true, only summary fields will be returned.
        :param staticDataOnly: If true, only static data will be returned.

        :return: A list of rules (JSON objects).
        """
        try:
            response = self.client.get(
                "/rules", params={"prefix": prefix, "tags": tags, "summary": summary, "staticDataOnly": staticDataOnly})

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

    def createRule(self, ruleData: dict):
        """
        Creates a rule.

        :param ruleData: The rule data to be created (as a dictionary).

        :return: The created rule (JSON).
        """
        try:
            response = self.client.post(
                "/rules", data=json.dumps(ruleData), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Creation refused: Missing required parameter."}
            elif status_code == 409:
                return {"error": "Creation refused: Rule with the same UID already exists."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 201:
            location = response.headers.get("Location")
            return {
                "message": "Rule successfully created.",
                "location": location if location else "No Location header provided."
            }
        elif status_code == 400:
            return {"error": "Creation refused: Missing required parameter."}
        elif status_code == 409:
            return {"error": "Creation refused: Rule with the same UID already exists."}

        return {"error": f"Unexpected response: {status_code}"}

    def getRule(self, ruleUID: str):
        """
        Gets the rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to retrieve.

        :return: The rule object (JSON).
        """
        try:
            response = self.client.get(f"/rules/{ruleUID}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateRule(self, ruleUID: str, ruleData: dict):
        """
        Updates an existing rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to update.
        :param ruleData: The new rule data (as a dictionary).

        :return: The updated rule (JSON).
        """
        try:
            response = self.client.put(
                f"/rules/{ruleUID}", data=json.dumps(ruleData), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteRule(self, ruleUID: str):
        """
        Removes an existing rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to delete.

        :return: The API response (status code).
        """
        try:
            response = self.client.delete(
                f"/rules/{ruleUID}", header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getModule(self, ruleUID: str, moduleCategory: str, moduleID: str):
        """
        Gets the rule's module corresponding to the given category and ID.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleID: The ID of the module.

        :return: The module (JSON).
        """
        try:
            response = self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}", header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}

        return {"error": f"Unexpected response: {status_code}"}

    def getModuleConfig(self, ruleUID: str, moduleCategory: str, moduleID: str):
        """
        Gets the module's configuration.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleID: The ID of the module.

        :return: The module configuration (JSON).
        """
        try:
            response = self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}

        return {"error": f"Unexpected response: {status_code}"}

    def getModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleID: str, param: str):
        """
        Gets the module's configuration parameter.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleID: The ID of the module.
        :param param: The name of the configuration parameter.

        :return: The configuration parameter value (JSON).
        """
        try:
            response = self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config/{param}", header={'Accept': 'text/plain'})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}

        return {"error": f"Unexpected response: {status_code}"}

    def setModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleID: str, param: str, value: str):
        """
        Sets the module's configuration parameter value.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleID: The ID of the module.
        :param param: The name of the configuration parameter.
        :param value: The value to set for the configuration parameter.

        :return: The API response (status code).
        """
        try:
            response = self.client.put(f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config/{param}",
                                       data=json.dumps(value), header={'Content-Type': 'text/plain'})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found or does not have a module with such Category and ID."}

        return {"error": f"Unexpected response: {status_code}"}

    def getActions(self, ruleUID: str):
        """
        Gets the rule actions.

        :param ruleUID: The UID of the rule.

        :return: A list of actions (JSON).
        """
        try:
            response = self.client.get(f"/rules/{ruleUID}/actions")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getConditions(self, ruleUID: str):
        """
        Gets the rule conditions.

        :param ruleUID: The UID of the rule.

        :return: A list of conditions (JSON).
        """
        try:
            response = self.client.get(f"/rules/{ruleUID}/conditions")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getConfiguration(self, ruleUID: str):
        """
        Gets the rule configuration values.

        :param ruleUID: The UID of the rule.

        :return: The configuration of the rule (JSON).
        """
        try:
            response = self.client.get(f"/rules/{ruleUID}/config")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def updateConfiguration(self, ruleUID: str, configData: dict):
        """
        Sets the rule configuration values.

        :param ruleUID: The UID of the rule.
        :param configData: The new configuration data (as a dictionary).

        :return: The updated configuration (JSON).
        """
        try:
            response = self.client.put(f"/rules/{ruleUID}/config", data=json.dumps(
                configData), header={"Content-Type": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def setRuleState(self, ruleUID: str, enable: bool):
        """
        Sets the rule configuration values. Activates or deactivates the rule.

        :param ruleUID: The UID of the rule.
        :param enable: If true, the rule will be activated. If false, the rule will be deactivated.

        :return: The API response (status code).
        """
        try:
            response = self.client.post(f"/rules/{ruleUID}/enable", data="true" if enable else "false", header={
                                        "Content-Type": "text/plain; charset=utf-8", "Accept": "text/plain"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def enableRule(self, ruleUID: str):
        return self.setRuleState(ruleUID, True)

    def disableRule(self, ruleUID: str):
        return self.setRuleState(ruleUID, False)

    def runNow(self, ruleUID: str, contextData: dict = None):
        """
        Executes the rule's actions immediately.

        :param ruleUID: The UID of the rule.
        :param contextData: Optional context data for executing the rule.

        :return: The API response (status code).
        """
        try:
            response = self.client.post(
                f"/rules/{ruleUID}/runnow", data=json.dumps(contextData) or {})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def getTriggers(self, ruleUID: str):
        """
        Gets the rule triggers.

        :param ruleUID: The UID of the rule.

        :return: A list of triggers (JSON).
        """
        try:
            response = self.client.get(f"/rules/{ruleUID}/triggers")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Rule corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule corresponding to the given UID does not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def simulateSchedule(self, fromTime: str, untilTime: str):
        """
        Simulates the executions of rules filtered by tag 'Schedule' within the given times.

        :param fromTime: Simulates the executions of rules filtered by tag 'Schedule' within the given times.
        :param untilTime: Simulates the executions of rules filtered by tag 'Schedule' within the given times.

        :return: The simulation results (JSON).
        """
        try:
            response = self.client.get("/rules/schedule/simulations", params={
                                       "from": fromTime, "until": untilTime}, header={'Accept': 'application/json'})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "The max. simulation duration of 180 days is exceeded."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "The max. simulation duration of 180 days is exceeded."}

        return {"error": f"Unexpected response: {status_code}"}

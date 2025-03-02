"""
Simple wrapper lib to interface with the lan game mode found here:
https://developer.lovense.com/docs/standard-solutions/standard-api.html#game-mode
Direct the user to Lovense Remote App > Discover > Game Mode > Enable LAN
Get the user info about Local IP, and Port and feed it into LovenseGameMode
class constructor. The "Accepting control from third-party apps"
should show your app name. The home tab section should also say "Toy controlled
by" your app name.
"""
import json
import time
import logging
import requests
from typing import Any, Dict, List, Optional, Union
from enum import StrEnum

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


class Actions(StrEnum):
    """Data class to hold the magic string values for Actions"""
    VIBRATE = "Vibrate"
    VIBRATE1 = "Vibrate1"
    VIBRATE2 = "Vibrate2"
    VIBRATE3 = "Vibrate3"
    ROTATE = "Rotate"
    PUMP = "Pump"
    THRUSTING = "Thrusting"
    FINGERING = "Fingering"
    SUCTION = "Suction"
    DEPTH = "Depth"
    ALL = "All"


class Presets(StrEnum):
    """Data class to hold the magic string values for Presets"""
    PULSE = "pulse"
    WAVE = "wave"
    FIREWORKS = "fireworks"
    EARTHQUAKE = "earthquake"


class GameModeWrapper():
    """
    ## API wrapper to deal with the LAN/Game Mode version of the Lovense
    Standard Solutions API

    ### Args:
    - app_name: The name of your application.
    - local_ip: the ip of the device to connect to
    - port: the port of the device to connect to
    - ssl_port: unused but in the Lovense app
    - log: enable logging in the class

    ### Methods:
    - send_command(): Send a JSON command directly to the app (advanced)
    - get_toys(): Gets the toy(s) connect to the Lovense app
    - get_toys_name(): Same as get_toys() but just the name of the devices
    - function_request(): Send a single Pattern immediately
    - stop(): Sends a stop immediately command
    - pattern_request(): Avoids network pressure of multiple function commands
    - pattern_request_raw(): More api accurate version for patterns (advanced)
    - preset_request(): Send one of the pre-made or user created patterns
    - decode_response(): Make the return value of any command more readable.

    ### Attributes
    - app_name: The name of the app
    - api_endpoint: The destination the data is sent to
    - actions: a reference to the Actions StrEnum
    - presets: a reference to the Presets StrEnum
    - error_codes: A dict of all the expected error codes
    """

    def __init__(
        self,
        app_name: str,
        local_ip: str,
        port: int = 20010,
        ssl_port: int = 30010,
        log: bool = False
    ) -> None:

        # Define the server's API endpoint
        self.app_name = app_name
        self.api_endpoint = f"http://{local_ip}:{port}/command"
        self._ssl_port = ssl_port

        # Set up the logger
        self.logger = logging.getLogger(__name__)

        # References to the StrEnums
        self.actions = Actions
        self.presets = Presets

        # the last command sent, can be used to send again
        self.last_command = None

        # A list of all the error code from the docs
        self.error_codes = {
            200: "OK",
            400: "Invalid Command",
            401: "Toy Not Found",
            402: "Toy Not Connected",
            403: "Toy Doesn't Support This Command",
            404: "Invalid Parameter",
            500: "HTTP server not started or disabled",
            506: "Server Error. Restart Lovense Connect."
        }

        # clamp values for the function_request
        self._function_range = {
            Actions.VIBRATE: {"min": 0, "max": 20},
            Actions.VIBRATE1: {"min": 0, "max": 20},
            Actions.VIBRATE2: {"min": 0, "max": 20},
            Actions.VIBRATE3: {"min": 0, "max": 20},
            Actions.ROTATE: {"min": 0, "max": 20},
            Actions.PUMP: {"min": 0, "max": 3},
            Actions.THRUSTING: {"min": 0, "max": 20},
            Actions.FINGERING: {"min": 0, "max": 20},
            Actions.SUCTION: {"min": 0, "max": 20},
            Actions.DEPTH: {"min": 0, "max": 3},
            Actions.ALL: {"min": 0, "max": 20}
        }

    def _parse_json(
        self,
        data: Union[str, dict, list]
    ) -> Dict[str, Any]:
        """refactor request for nested encoded objects into json/dict objects

        Args:
            data (str | dict | list): The data to parse, can be a JSON string.

        Returns:
            Dict[str, Any]: The refactored json data
        """
        if isinstance(data, str):
            try:
                return json.loads(data)
            except ValueError:
                return data  # type: ignore
        elif isinstance(data, dict):
            return {k: self._parse_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._parse_json(item) for item in data]  # type: ignore
        else:
            return data

    def send_command(
        self,
        command_data: Dict[str, Any],
        timeout: int = 10,
        retries: int = 3,
        retry_delay: int = 5
    ) -> Optional[Dict[str, Any]]:
        """Directly send a json command to the app and handle the response.

        Args:
            command_data (Dict[str, Any]): Json value to send to the app
            timeout (int): Timeout for the request in seconds
            retries (int): Number of retries if the request fails
            retry_delay (int): Delay between retries in seconds

        Returns:
            Optional[Dict[str, Any]]: The json response code from the app
        """
        headers = {
            "X-platform": self.app_name
        }

        time_sec = command_data.get("timeSec")
        if time_sec is not None and time_sec != 0:
            clamped_time = max(1, min(time_sec, 6000))
            command_data.update({'timeSec': clamped_time})

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Sending command: {command_data}")

        self.last_command = command_data

        for attempt in range(retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    json=command_data,
                    headers=headers,
                    timeout=timeout
                )
                if response.status_code == 200:
                    response_json = response.json()
                    response_json = self._parse_json(response_json)
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug(self.decode_response(response_json))
                    return response_json
                else:
                    self.logger.error(
                        f"Received HTTP status code {response.status_code} from the server."
                    )
            except requests.exceptions.ConnectionError:
                self.logger.error("Failed to establish a new connection")
            except requests.exceptions.Timeout:
                self.logger.error("Request timed out")
            except requests.exceptions.RequestException:
                self.logger.error("An error occurred in the request")

            if attempt < retries - 1:
                self.logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        self.logger.error("Max retries exceeded. Command failed.")
        return None

    def _function_clamp_range(
        self, actions: Dict[str, float] | dict[Actions, float]
    ) -> Dict[str, float]:
        """Clamp the values of actions within API specified ranges.

        Args:
            actions (Dict[str, int]): A dictionary containing actions as keys
                and their corresponding integer values.

        Returns:
            Dict[str, int]: A dictionary containing clamped values of actions.
        """
        clamped_actions = {}
        for action, value in actions.items():
            if action in self._function_range:
                min_val = self._function_range[action]["min"]
                max_val = self._function_range[action]["max"]
                clamped_value = max(min(value, max_val), min_val)
                clamped_actions[action] = clamped_value
            else:
                clamped_actions[action] = value
        return clamped_actions

    def function_request(
        self,
        actions: Dict[str, float] | dict[Actions, float],
        time: float = 0,
        loop_on_time: Optional[float] = None,
        loop_off_time: Optional[float] = None,
        toy_id: Optional[str] = None,
        stop_last: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """Send a function request to the app

        Args:
            actions (Dict[str, int]): A dictionary containing actions as keys
                and their corresponding values. Use the `Actions` StrEnum.
            time (float, optional): The time in seconds for the function
                request. Defaults to 0 for indefinite time.
            loop_on_time (Optional[float], optional): The time in seconds for
                a running loop. Defaults to None.
            loop_off_time (Optional[float], optional): The time in seconds for
                the loop to pause. Defaults to None.
            toy_id (Optional[str], optional): The ID of the toy. Defaults to
                None for all devices.
            stop_last (Optional[bool], optional): Whether to stop the previous
                command. Defaults to None for yes stop.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the response
                if the command is sent successfully, otherwise None.
        """
        actions = self._function_clamp_range(actions)
        action = ','.join(f"{key}:{value}" for key, value in actions.items())

        payload = {
            "command": "Function",
            "action": action,
            "timeSec": time,
            "apiVer": 1
        }

        if loop_on_time is not None:
            payload["loopRunningSec"] = max(loop_on_time, 1)
        if loop_off_time is not None:
            payload["loopPauseSec"] = max(loop_off_time, 1)
        if toy_id is not None:
            payload["toy"] = toy_id
        if stop_last is not None:
            payload["stopPrevious"] = 1 if stop_last else 0

        return self.send_command(payload)

    def stop(self, toy_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Send a command to stop a function.

        Args:
            toy_id (Optional[str], optional): the ID of the toy to stop.
                Defaults to None for all toys.
        Returns:
            Optional[Dict[str, Any]]:
        """
        payload = {
            "command": "Function",
            "action": "Stop",
            "timeSec": 0,
            "apiVer": 1
        }
        if toy_id is not None:
            payload["toy"] = toy_id
        return self.send_command(payload)

    def _convert_actions_to_letters(
        self,
        actions: Union[list[str], list[Actions]]
    ) -> str:
        """Convert a list of action identifiers to a string of their
            corresponding letter codes.

        Args:
            actions (Union[list[str], list[Actions]]): A list of actions
                as either strings or instances of the `Actions` StrEnum.

        Returns:
            str: A comma-separated string of valid letter codes derived from
                the input actions. An empty string is returned for errors.
        """
        letter_codes = []
        valid_letters = ["v", "r", "p", "t", "f", "s", "d"]

        for action in actions:
            if isinstance(action, str) and len(action) > 0:
                letter = action[0].lower()
                if letter not in valid_letters:
                    continue
                letter_codes.append(letter)
            elif isinstance(action, Actions):
                letter_codes.append(action[0].lower())
            else:
                return ""

        if letter_codes:
            return ','.join(letter_codes)
        return ""

    def pattern_request_raw(
        self,
        strength: str,
        rule: str = "V:1;F:;S:100#",
        time: float = 0,
        toy_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create and send a pattern request to a toy using raw rules and
            strengths strings.

        Args:
            strength (str): The strength string defining the pattern.
            rule (str, optional): The rule string defining the pattern.
                Defaults to "V:1;F:;S:100#".
                Rules format:
                    V:1; | version,
                    F:(...); | Features (Actions letter) comma separated,
                    S:100# | Interval 100ms
            time (float, optional): The duration of the pattern in seconds.
                Defaults to 0.
            toy_id (Optional[str], optional): The ID of the toy. Defaults to
                None for all devices.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the response
                if the command is sent successfully, otherwise None.
        """
        payload = {
            "command": "Pattern",
            "rule": rule,
            "strength": strength,
            "timeSec": time,
            "apiVer": 2
        }

        if toy_id is not None:
            payload["toy"] = toy_id

        return self.send_command(payload)

    def pattern_request(
        self,
        pattern: List[int],
        actions: Union[List[str], List[Actions], None] = None,
        interval: int = 100,
        time: float = 0,
        toy_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Create and send a pattern request to a toy using abstracted parameters.

        Args:
            pattern (List[int]):  A list of integers representing the pattern
                strength over time. Limited to the first 50 elements.
            actions (Union[List[str], List[Actions], None], optional): A list
                of action identifiers (strings or Actions instances).
                Defaults to [Actions.ALL] if None.
            interval (int, optional): The interval between actions in
                milliseconds. Clamped between 100 and 1000. Defaults to 100.
            time (float, optional): The duration of the pattern in seconds.
                Defaults to 0.
            toy_id (Optional[str], optional): The ID of the toy. Defaults to
                None for all devices.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the response
                if the command is sent successfully, otherwise None.
        """
        if actions is None:
            actions = [Actions.ALL]

        pattern = pattern[:50]
        pattern = [min(max(0, num), 20) for num in pattern]

        interval = min(max(interval, 100), 1000)

        acts = self._convert_actions_to_letters(actions)
        rule = f"V:1;F:{acts};S:{interval}#"

        if Actions.ALL in actions:
            rule = f"V:1;F:;S:{interval}#"
        strength = ";".join(map(str, pattern))

        return self.pattern_request_raw(strength, rule, time, toy_id)

    def preset_request(
        self,
        name: str,
        time: float = 0,
        toy_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Sends a preset command to the toy.

        Args:
            name (str): The name of the preset. This can be a default preset
                from the `Presets` enum or a custom preset added by the user.
            time (float, optional): The duration for which the preset should
                be active, in seconds. Defaults to 0 for indefinite time.
            toy_id (Optional[str], optional): The ID of the toy. Defaults to
                None for all devices.
        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the response code
                and type, or None if the command fails.
        """
        payload = {
            "command": "Preset",
            "name": name,
            "timeSec": time,
            "apiVer": 1
        }

        if toy_id is not None:
            payload["toy"] = toy_id

        return self.send_command(payload)

    def get_toys(self) -> Optional[Dict[str, Any]]:
        """Send a command to retrieve information about all toys.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing information
                about all toys, or None if an error occurred.
        """
        return self.send_command({
            "command": "GetToys"
        })

    def get_toys_name(self) -> Optional[Dict[str, Any]]:
        """Send a command to retrieve names of all toys

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing names of all
                toys, or None if an error occurred.
        """
        return self.send_command({
            "command": "GetToyName"
        })

    def decode_response(self, response: Optional[Dict[str, Any]]) -> str:
        """
        Decode any commands response from the app into a human readable string

        Args:
            response (Optional[Dict[str, Any]]): Response returned of a command

        Returns:
            str: A human readable string
        """
        if response is None:
            return "No response received from the app."

        response_type = response.get('type', "Not Response")
        return_str = f"Response from the app: {response_type}\n"

        code = response.get('code')
        if isinstance(code, int):
            error_message = self.error_codes.get(
                code, "Unknown Error"
            )
            code_message = f"{error_message}, {code}"
        else:
            code_message = f"Unknown response code {code}"
        return_str += f"Response from the toy: {code_message}\n"

        data = response.get('data')
        if data is not None:
            return_str += f"Data: {json.dumps(data, indent=4)}"

        return return_str

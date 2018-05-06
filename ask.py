import json
import subprocess

class AskCli:

    def __init__(self, skill_id=None, locale="en-US", skill_dir=None):
        self.skill_id = skill_id
        self.locale = locale
        self.skill_dir = skill_dir

    @property
    def _cmd_base(self):
        return ["ask", "simulate"]

    def _make_cmd(self, text, locale=None):
        cmd = self._cmd_base
        if self.skill_id:
            cmd.extend(["-s", self.skill_id])
        cmd.extend(["-l", locale or self.locale])
        cmd.extend(["-t", "alexa {}".format(text)])
        return cmd

    def simulate(self, text):
        cmd = self._make_cmd(text)
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=self.skill_dir)
        return AlexaSimulateResponse(process)


class AlexaSimulateResponse:

    def __init__(self, process):
        try:
            self._response = json.loads(process.stdout)
        except json.decoder.JSONDecodeError as e:
            raise AlexaSimulateError("Could not parse simulate response: \"{}\"".format(process.stdout))

    @property
    def simulation_id(self):
        return self._response.get("id")

    @property
    def successful(self):
        return self._response.get("status") == "SUCCESSFUL"

    @property
    def _result(self):
        return self._response.get("result", {})

    @property
    def error_message(self):
        return not self.successful and self._result.get("error", {}).get("message") or None

    @property
    def invocation_request(self):
        return self._result.get("skillExecutionInfo", {}).get("invocationRequest", {})

    @property
    def intent(self):
        intent = self.invocation_request.get("body", {}).get("request", {}).get("intent", {})
        return intent and SimulateIntent(intent) or None


class SimulateIntent:

    def __init__(self, intent_info):
        self._intent_info = intent_info

    @property
    def name(self):
        return self._intent_info.get("name")

    @property
    def slots(self):
        slots = {}
        for slot_name, slot_info in self._intent_info.get("slots", {}).items():
            matched_id, matched_name = self._get_resolution_matches(slot_info.get("resolutions", {}))
            slots[slot_name] = {
                "value": slot_info.get("value"),
                "matched_id": matched_id,
                "matched_name": matched_name
            }
        return slots

    def _get_resolution_matches(self, resolutions):
        resolutions_per_authority = resolutions.get("resolutionsPerAuthority", [])
        if resolutions_per_authority:
            resolution = resolutions_per_authority[0]
            if resolution.get("status", {}).get("code") == "ER_SUCCESS_MATCH":
                values = resolution.get("values")
                if values:
                    value = values[0].get("value", {})
                    return value.get("id"), value.get("name")
        return None, None


class AlexaSimulateError(Exception):
    pass

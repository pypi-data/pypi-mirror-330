"""
Contains helpers for interacting with Skyramp testing scenarios.
"""

from typing import Optional

from typing_extensions import Self
from skyramp.utils import _get_rest_path_name
from skyramp.test_request2 import RequestV2


class AsyncRequest:
    """' Wrapper class for RequestV2 object"""

    def __init__(self, scenario, request, step_index):
        self.scenario = scenario
        self.request = request
        self.step_index = step_index

    def get_async_request_value(self, path):
        """
        returns request's response value construct for asynchronous backend
        """
        return f"requests.{self.request.name}.res.{path}"

    def request_status_check(self, code):
        """
        returns if construct for asynchronous backend
        """
        return f"requests.{self.request.name}.code == {code}"

    def set_async_var(self, var_name, value):
        """
        construct backend interpretation of updating scenario vars
        """
        # if current step is a request, update the request with the var override
        if (
            len(self.scenario.steps) > self.step_index
            and self.scenario.steps[self.step_index]["type"] == "request"
        ):
            self.scenario.steps[self.step_index]["varOverride"][var_name] = value
            if var_name not in self.scenario.vars:
                self.scenario.vars[var_name] = ""


class AsyncScenario:
    """
    Represents a testing scenario.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.steps = []
        self.vars = {}
        self.until = ""
        self.max_retries = 5
        self.retry_interval = 1

    # pylint: disable=too-many-locals
    def add_async_request(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None,
        body: Optional[str] = None,
        headers: Optional[dict] = None,
        path_params: Optional[dict] = None,
        query_params: Optional[dict] = None,
        form_params: Optional[dict] = None,
        multipart_params: Optional[list] = None,
        data_override: Optional[dict] = None,
        description: Optional[str] = None,
        expected_code: Optional[str] = None,
    ):
        """
        Adds an asynchronous request to this scenario.

        Args:
            url: The URL of the request
            path: The path of the request
            method: The HTTP method of the request (e.g., GET, POST)
            body: The body of the request
            headers: The headers of the request
            path_params: The path parameters of the request
            query_params: The query parameters of the request
            form_params: The form parameters of the request
            multipart_params: The multipart parameters of the request
            data_override: The data override for the request
            description: The description of the request
            expected_code: The expected HTTP status code of the request
        """
        request = RequestV2(
            name=name,
            url=url,
            path=path,
            method=method,
            body=body,
            headers=headers,
            path_params=path_params,
            query_params=query_params,
            form_params=form_params,
            multipart_params=multipart_params,
            data_override=data_override,
            description=description,
            expected_code=expected_code,
        )
        if not name:
            request.name = _get_rest_path_name(path, method)
        step_request = request.as_request_dict()
        step_request["type"] = "request"
        step_request["varOverride"] = {}
        step_request["varExport"] = {}
        self.steps.append(step_request)
        step_index = len(self.steps) - 1
        return AsyncRequest(self, request, step_index)

    def add_async_scenario(
        self,
        nested_scenario: Self,
        until: Optional[str] = "",
        max_retries: Optional[int] = 5,
        retry_interval: Optional[int] = 1,
    ):
        """
        Adds an asynchronous nested scenario to this scenario.

        Args:
            nested_scenario: The nested scenario to add
            until: The condition to stop retrying
        """
        scenario = nested_scenario
        step_scenario = {
            "type": "scenario",
            "scenario": scenario,
        }
        self.until = until
        if self.until != "":
            self.max_retries = max_retries
            self.retry_interval = retry_interval
        self.steps.append(step_scenario)

    def set_async_var(self, var_name, value):
        """
        construct backend interpretation of updating scenario vars
        """
        if self.vars is None:
            self.vars = {}
        self.vars[var_name] = value

    def get_async_var(self, var_name):
        """
        construct backend interpretation of accessing scenario vars
        """
        return f"vars.{var_name}"

    def get_async_scenario_value(self, var):
        """
        returns scenario's response value construct for asynchronous backend
        """
        return f"scenarios.{self.name}.{var}"

    def export_async_var(self, var_name, value):
        """
        construct backend interpretation of updating scenario vars
        """
        self.steps.append({"type": "varExport", "name": var_name, "value": value})

    def to_json(self):
        """
        Converts this scenario to JSON.
        """
        # iterate through the steps and convert them to JSON
        steps = []
        for step in self.steps:
            if step["type"] == "request":
                steps.append({"request": step})
            elif step["type"] == "scenario":
                if isinstance(step["scenario"], AsyncScenario):
                    steps.append({"scenario": step["scenario"].to_json()})
        return {
            "name": self.name,
            "steps": steps,
            "vars": self.vars,
            "until": self.until,
            "maxRetries": self.max_retries,
            "interval": self.retry_interval,
        }

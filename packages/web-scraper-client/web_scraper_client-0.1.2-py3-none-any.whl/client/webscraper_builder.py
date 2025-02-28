import requests
from requests import Response

from client.enums.api_instruction_action_type import ApiInstructionActionType
from client.enums.api_instruction_block_type import ApiInstructionBlockType
from client.enums.api_instruction_element_type import ApiInstructionElementType
from client.enums.api_instruction_identificator_type import ApiInstructionIdentificatorType
from client.models.driver_options import DriverOptions
from client.util.exceptions import ScrapeException


class WebScraperBuilder:
    def __init__(self, url: str, api_key: str):
        self._url = url
        self._api_key = api_key
        self._instructions: list[object] = []

    def wait(self, seconds: int, by: ApiInstructionIdentificatorType, wait_for: ApiInstructionElementType,
             element_id: str, ignore_error: bool = False):
        self._instructions.append({
            'action_type': ApiInstructionActionType.WAIT.value,
            'action_value': {
                'seconds': seconds,
                'by': by.value,
                'wait_for': wait_for.value,
                'id': element_id
            },
            'action_ignore_error': ignore_error
        })
        return self

    def find(self, by: ApiInstructionIdentificatorType, element_id: str, ignore_error: bool = False):
        self._instructions.append({
            'action_type': ApiInstructionActionType.FIND.value,
            'action_value': {
                'by': by.value,
                'id': element_id
            },
            'action_ignore_error': ignore_error
        })
        return self

    def click(self, ignore_error: bool = False):
        self._instructions.append({
            'action_type': ApiInstructionActionType.CLICK.value,
            'action_ignore_error': ignore_error
        })
        return self

    def scroll(self, block: ApiInstructionBlockType, ignore_error: bool = False):
        self._instructions.append({
            'action_type': ApiInstructionActionType.SCROLL.value,
            'action_value': {
                'block': block.value
            },
            'action_ignore_error': ignore_error
        })
        return self

    def get(self, page_url: str, options: DriverOptions | None = None) -> Response:
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self._api_key
        }

        data = {
            'url': page_url,
            'options': options.__dict__() if options is not None else None,
            'instructions': self._instructions
        }

        response = requests.post(url=f'{self._url}/api/v1/query', json=data, headers=headers)

        if response.status_code == 500:
            raise ScrapeException(response.text)

        response.raise_for_status()

        return response.json()['response']


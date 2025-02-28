from enum import Enum


class ApiInstructionActionType(Enum):
    WAIT = 'wait'
    SCROLL = 'scroll'
    CLICK = 'click'
    FIND = 'find'

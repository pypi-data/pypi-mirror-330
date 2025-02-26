'''dict.py'''

from enum import Enum
from datetime import datetime
from sslib.helper.string import StringHelper


class DictEx:
    '''DictEx'''

    def to_dict(self, include_none: bool = False, camel_case: bool = True) -> dict:
        '''to_dict'''
        output = {}
        for k, v in self.__dict__.items():
            if not include_none and v is None:
                continue
            if camel_case:
                k = StringHelper.camel_case(k)
            output[k] = self._convert(v)
        return output

    def _convert(self, source: any) -> any:
        if isinstance(source, datetime):
            return StringHelper.datetime(source)
        if isinstance(source, Enum):
            return source.value
        return source

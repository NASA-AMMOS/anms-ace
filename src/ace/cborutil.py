#
# Copyright (c) 2023 The Johns Hopkins University Applied Physics
# Laboratory LLC.
#
# This file is part of the Asynchronous Network Managment System (ANMS).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This work was performed for the Jet Propulsion Laboratory, California
# Institute of Technology, sponsored by the United States Government under
# the prime contract 80NM0018D0004 between the Caltech and NASA under
# subcontract 1658085.
#
''' Utilities to convert to CBOR diagnostic notation.
'''
import base64
import math


def to_diag(val) -> str:
    ''' Convert a Python object to CBOR diagnostic notation.
    '''
    diag = None
    if val is None:
        diag = 'null'
    elif isinstance(val, bool):
        diag = 'true' if val else 'false'
    elif isinstance(val, int):
        diag = f'{val}'
    elif isinstance(val, float):
        # Special names from https://www.rfc-editor.org/rfc/rfc8949#name-diagnostic-notation
        if math.isnan(val):
            diag = 'NaN'
        elif not math.isfinite(val):
            diag = 'Infinity'
            if val < 0:
                diag = '-' + diag
        else:
            diag = f'{val}'
    elif isinstance(val, str):
        diag = f'"{val}"'
    elif isinstance(val, bytes):
        diag = f'h\'{val.hex()}\''
    else:
        raise ValueError(f'No CBOR diagnostic converstion for type {type(val)}: {val}')
    return diag


def to_hexstr(data: bytes) -> str:
    ''' Convert a byte string into hexstr text.

    :param data: The byte string.
    :return: Encoded text.
    '''
    return '0x' + base64.b16encode(data).decode('ascii')


def from_hexstr(text: str) -> bytes:
    ''' Convert hexstr text into byte string.

    :param text: The hexstring.
    :return: Decoded bytes.
    '''
    if text[0:2].casefold() != '0x':
        raise ValueError(f'hexstr must start with 0x, got:{text}')
    return base64.b16decode(text[2:], casefold=True)

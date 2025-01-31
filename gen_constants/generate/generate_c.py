from typing import TextIO

from ..__version__ import VERSION
from ..config import Constants


def generate(constants: Constants, f: TextIO) -> None:
    f.write(
        f'''\
/* This file was auto-generated by v{VERSION} of {__package__} */
#pragma once

#ifdef __cplusplus
extern "C" {{
#endif

'''
    )

    if constants.constants:
        f.write(
            '''
/********************************************************************************
 * Constants
 *******************************************************************************/
'''
        )

    for constant in constants.constants:
        f.write(f'#define {constant.name.upper()} {constant.value}\n')

    if constants.anonymous_enums:
        f.write(
            '''
/********************************************************************************
 * Anonymous enums
 *******************************************************************************/
'''
        )

    for enum in constants.anonymous_enums:
        f.write(
            '''
enum {
'''
        )
        for key, value in enum.values.items():
            f.write(
                f'''\
    {key.upper()} = {hex(value)}, /* {value} */
'''
            )

        f.write('};\n')

    if constants.named_enums:
        f.write(
            '''
/********************************************************************************
 * Named enums
 *******************************************************************************/
'''
        )

    for enum_name, enum in constants.named_enums.items():
        f.write(
            f'''
typedef enum {enum_name} {{
'''
        )
        for key, value in enum.values.items():
            f.write(
                f'''\
    {enum_name.upper()}_{key.upper()} = {hex(value)}, /* {value} */
'''
            )

        f.write(f'}} {enum_name}_t;\n')

    f.write(
        '''
#ifdef __cplusplus
}
#endif
'''
    )

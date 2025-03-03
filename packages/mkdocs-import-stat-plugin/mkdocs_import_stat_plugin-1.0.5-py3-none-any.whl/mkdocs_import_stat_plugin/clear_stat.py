
import re

reg = r'^(\s*```\w+)(.*)$'

def match_clear(line: str) -> str | None:
    """只保留有效部分，保证与 markdown enhanced 插件兼容

    Args:
        str (str): _description_

    Returns:
        str: _description_
    """
    matches = re.findall(reg, line)
    for elem in matches:
        # 后方有非必要数据 如 ```py {cmd=xx a=b c} 才进行替换，否则不管
        if elem[1]: 
            return elem[0]
    return None
    
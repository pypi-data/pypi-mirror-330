from os import path
import re

from mkdocs.structure.pages import Page


reg = r'^(\s*)@import "(.*?)"\s*(?:{(.+)})?\s*$'

def match_import(line: str, page: Page) -> str | None:
    """是否匹配import语义

    Args:
        line (str): 该行的内容

    Returns:
        str | None: 得到的内容，否则为空
    """
    
    matches = re.findall(reg, line)
    res = None
    for elem in matches:
        tab_str = elem[0]
        file_path_name: str = elem[1]
        config = get_config(elem[2])
        p_dir = config.get('p_dir') 
        is_abs = config.get('abs_path')
        if not path.isabs(file_path_name):
            if p_dir:
                file_path_name = path.join(p_dir, file_path_name)
            file_path_name = path.join(page.file.src_dir, file_path_name)
        elif not is_abs:
            file_path_name = path.join(page.file.src_dir, file_path_name.removeprefix('/'))
        
        res = parse_content(tab_str, file_path_name, config)
        # print('res:', res)
    
    return res

reg_config = r'(\w+)\s*=\s*(\w+(\.\w*)?|"[^"]*"|\'[^\']*\')|(\w+)'

def get_config(config_str: str) -> dict:
    """解析配置

    Args:
        config_str (str): 配置字符串

    Returns:
        dict: 配置字典 
            p_dir 上级路径
            abs_path 绝对路径
    """    
    matches = re.findall(reg_config, config_str, flags=re.DOTALL)

    data = {}
    for match in matches:
        key = match[0] or match[3]
        value = match[1] or 'true'  # 如果没有显式赋值，默认为 'true'

        # 尝试将值转换为整数、浮点数、布尔值或字符串
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.lower() == 'null':
                    value = None
                else:
                    # 去掉引号并保存为字符串
                    value = value.strip('\"\'')
        data[key] = value
    return data

def parse_content(tab_str: str, file_path_name: str, config: dict) -> str:
    """解析文件内容并根据配置截取部分内容。

    Args:
        tab_str (str): 用于连接各行的字符串。
        file_path_name (str): 文件的路径和名称。
        config (dict): 配置字典，包含 'line_begin' 和 'line_end' 键。

    Returns:
        str: 截取后的内容，使用 `tab_str` 连接各行。
    """
    line_begin = config.get('line_begin', 0)
    line_end = config.get('line_end')
    tab = config.get('tab', '')
    if tab:
        tab_str = '    '
    res = ''
    with open(file_path_name, 'r') as f:
        lines = f.readlines()
        if line_end:
            lines = lines[line_begin:line_end]
        else:
            lines = lines[line_begin:]
        res = f'\n{tab_str}'.join(lines)
        
    if not res:
        return ''
        
    base_name = path.basename(file_path_name)
    _, ext = path.splitext(base_name)
    ext = ext[1:]
    as_ext = config.get('as') or ext
    
    return f'{tab_str}```{as_ext}\n{tab_str}{res}\n{tab_str}```'
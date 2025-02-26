import json
import io
import os
import html_to_json
import demjson3
import yaml
import re
import base64

#print("load json")

def handle_bytes(obj):
    if isinstance(obj, bytes):
        try:
            # 尝试用 UTF-8 解码
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            # 如果失败，转为 Base64
            return base64.b64encode(obj).decode('utf-8')
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def Dumps(obj, indent=4, ensure_ascii=False) -> str:
    """
    It takes a Python object and returns a JSON string
    
    :param obj: The object to be serialized
    :param indent: This is the number of spaces to indent for each level. If it is None, that
    will insert newlines but won't indent the new lines, defaults to 4 (optional)
    :param ensure_ascii: If True, all non-ASCII characters in the output are escaped with \\uXXXX
    sequences, and the result is a str instance consisting of ASCII characters only. If False, some
    chunks written to fp may be unicode instances. This usually happens because the input contains
    unicode strings or the, defaults to False (optional)
    :return: A string
    """
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, default=handle_bytes)

def is_html(text):
    # 改进的正则表达式，匹配更严格的HTML标签
    html_pattern = re.compile(r'<[a-zA-Z][^>]*>|</[a-zA-Z][^>]*>')
    
    # 查找字符串中是否包含HTML标签
    if html_pattern.search(text):
        return True
    else:
        return False

def Loads(input_data:str|io.TextIOWrapper) -> list | dict:
    """
    The function `Loads` reads input data from either a file, string, or text stream, and attempts to
    parse it as JSON, YAML, or HTML format, raising an exception if none of these formats are detected.
    
    :param input_data: The `input_data` parameter in the provided code snippet can be either a string
    containing data, or an `io.TextIOWrapper` object representing a file-like object. The function
    `Loads` reads the content from the input data, checks if it is HTML, JSON, or YAML formatted data
    :type input_data: str|io.TextIOWrapper
    :return: The function `Loads` will return a list, dict, or raise an exception depending on the
    content of the input data. If the content is successfully converted from HTML to JSON, it will
    return the JSON data. If the content is valid JSON, it will return the JSON data. If the content is
    valid YAML, it will return the YAML data. If none of these conditions are met, it
    """
    # 判断输入类型是否为io.TextIOWrapper，如果是则读取内容为str
    if isinstance(input_data, io.TextIOWrapper):
        content = input_data.read()
    elif isinstance(input_data, str):
        # 判断字符串是否为文件路径
        if os.path.isfile(input_data):
            with open(input_data, "r") as file:
                content = file.read()
        else:
            content = input_data
    else:
        raise ValueError("Input must be a string or io.TextIOWrapper")

    # 判断内容是否为JSON
    try:
        data = demjson3.decode(content)
        return data
    except demjson3.JSONDecodeError:
        pass

    # 判断内容是否为YAML
    try:
        data = yaml.safe_load(content)
        if data is not None and isinstance(data, (dict, list)):
            return data
    except yaml.YAMLError:
        pass

    # 判断内容是否为HTML
    if is_html(content):
        try:
            data = html_to_json.convert(content)
            return data
        except Exception:
            pass

    # 如果都不是，抛出自定义异常
    raise Exception("Input is not a valid JSON, YAML, or HTML format")

def Valid(json_string:str) -> bool:
    """
    检查一个 JSON 字符串是否合法

    参数:
        json_string (str): 要检查的 JSON 字符串

    返回:
        bool: 如果 JSON 字符串合法则返回 True，否则返回 False
    """
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False

def ExtraValueByKey(obj:list|dict, key:str) -> list:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)

                if k == key:
                    arr.append(v)
                    
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def DeleteKeyContainString(obj:list|dict, target_string:str) -> dict|list:
    """
    遍历字典并删除包含特定字符串的键值对

    参数:
    d (dict): 需要遍历的字典
    target_string (str): 需要查找的字符串

    返回:
    dict: 删除包含目标字符串的键值对后的字典
    """
    keys_to_delete = [key for key in obj if target_string in key]

    for key in keys_to_delete:
        del obj[key]

    for key, value in obj.items():
        if isinstance(value, dict):
            DeleteKeyContainString(value, target_string)

    return obj

def DeleteKeyMatchString(obj:list|dict, target_string:str) -> dict|list:
    """
    遍历字典并删除等于特定字符串的键值对

    参数:
    d (dict): 需要遍历的字典
    target_string (str): 需要查找的字符串

    返回:
    dict: 删除等于目标字符串的键值对后的字典
    """
    keys_to_delete = [key for key in obj if target_string == key]

    for key in keys_to_delete:
        del obj[key]

    for key, value in obj.items():
        if isinstance(value, dict):
            DeleteKeyContainString(value, target_string)

    return obj

if __name__ == "__main__":
    # j = Dumps({1: 3, 4: 5})
    # print(j)

    # d = Loads(j)
    # print(d)

    # print(type(d))

    # ------------

    # data = {
    #     "key": {
    #         "key": [
    #             {
    #                 "a": "b"
    #             },
    #             {
    #                 "key": "123"
    #             }
    #         ]
    #     }
    # }

    # print(ExtraValueByKey(data, "key"))

    html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""

    print(Loads(html_string))
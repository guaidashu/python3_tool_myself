import json
import hashlib
import requests


# change the dict to a json str
def js_arr(text=None, id=None, reply=None):
    """
    This function is a tool which change the dict to a json str

    :param text: any type
    :param id: any type
    :param reply: any type
    :return: str
    """
    data = {'text': text, "id": id, 'reply': reply}
    return json.dumps(data)


# get a md5 str
def md5(s1):
    """
    This function can turn a str into a str which has been encrypted by md5

    :param s1: It's a str.
    :return: str
    """
    s = str(s1)
    h1 = hashlib.md5()
    h1.update(s.encode(encoding='utf-8'))
    s = h1.hexdigest()
    return s


# debug test
# noinspection PyRedundantParentheses,PyBroadException
def changeToStr(data, rowstr="<br>", count=4, origin_count=4):
    """
    This function can turn a data which you give into a str which you can look easily.
    Like a dict {"text": 1, "id":2, "reply":3}
    call the function changeToStr(text)
    you will look follow data:
    dict(3) =>{
      ["text"] => 1
      ["id"] => 2
      ["reply"] => 3
    }

    :param data: data you give, it can be any type.
    :param rowstr: it's a str. Enter, if you want to show data in web, it's default,
    or you want to show data in console, you should set rowstr="\n"
    :param count: It's a int. spacing num(I'm so sorry, I have forget the parameter's meaning, but you can try changing it.)
    :param origin_count: It's a int. spacing num(I'm so sorry, I have forget the parameter's meaning)
    :return: str
    """
    s = ""
    space1 = rowstr
    space2 = rowstr
    space = ""
    if count == 0:
        endstr = "}"
    else:
        endstr = "}"
    for i in range(count):
        space1 = space1 + " "
        if i >= origin_count:
            space2 = space2 + " "
    count = count + origin_count
    if isinstance(data, dict):
        length = len(data)
        s = s + "dict(" + str(length) + ") =>{"
        for k, v in data.items():
            s = s + space1 + "['" + str(k) + "'] => " + changeToStr(v, rowstr, count, origin_count)
        s = s + space2 + endstr
    elif isinstance(data, (tuple)):
        length = len(data)
        s = s + "tuple(" + str(length) + ") =>{"
        i = 0
        for v in data:
            s = s + space1 + "[" + str(i) + "] => " + changeToStr(v, rowstr, count, origin_count)
            i = i + 1
        s = s + space2 + endstr
    elif isinstance(data, (list)):
        length = len(data)
        s = s + "list(" + str(length) + ") =>{"
        i = 0
        for v in data:
            s = s + space1 + "[" + str(i) + "] => " + changeToStr(v, rowstr, count, origin_count)
            i = i + 1
        s = s + space2 + endstr
    else:
        s = str(data)
    return s


def formatData(data):
    return "<pre>" + changeToStr(data, rowstr="<br/>") + "</pre>"


def debug(data):
    print(changeToStr(data, rowstr="\n"))


def replace_html(s):
    s = s.replace('&quot;', '"')
    s = s.replace('&amp;', '&')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&nbsp;', ' ')
    s = s.replace(r'\/', '/')
    return s


# noinspection PyBroadException
def curlData(url, value=False, referer=False):
    """
    This function can get a web page's source data.

    :param url: str
    :param value: dict or default(None)
    :param referer: str
    :return: str(web page's source data)
    """
    headers = dict()
    headers['User-Agent'] = "baiduspider"
    headers['Cookie'] = ""
    headers['Accept'] = "*/*"
    headers['Connection'] = "keep-alive"
    if referer:
        headers['Referer'] = referer
    if value:
        res = requests.post(url, data=value, headers=headers)
    else:
        res = requests.get(url, headers=headers)
    try:
        data = res.content.decode("utf-8")
    except:
        try:
            data = res.content.decode("GBK")
        except:
            data = res.content
    return data


# noinspection PyBroadException
def getClientIp(request):
    """
    This function can get client ip.

    :param request: client request
    :return: str
    """
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip


# change dict which value & key is all bytes
# noinspection PyPep8Naming,PyBroadException
def byteToStr(data, dataType=None):
    """
    This function is born for happybase's data.
    Because happybase's data is all bytes.
    We should turn it into str(s) which has/have been decode.

    :param data: generator or other type's data.
    :param dataType: If you want to change other type's data, you should use default. Or set it to "generator"
    :return: type of source data
    """
    if dataType == "generator":
        result = list()
        for v in data:
            result.append(byteToStr(v))
        return result
    elif isinstance(data, tuple):
        result = list()
        for v in data:
            result.append(byteToStr(v))
        return tuple(result)
    elif isinstance(data, bytes):
        try:
            return data.decode("utf-8")
        except:
            try:
                return data.decode("GBK")
            except:
                return None
    elif isinstance(data, dict):
        return dict(map(byteToStr, data.items()))
    else:
        return data

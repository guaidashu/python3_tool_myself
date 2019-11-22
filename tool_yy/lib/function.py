import datetime
import json
import hashlib
import requests
import random
import time

# change the dict to a json str
# noinspection PyShadowingBuiltins
from tool_yy.config import settings


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


# get a sha1 str
def sha1(s1):
    """
        This function can turn a str into a str which has been encrypted by md5

        :param s1: It's a str.
        :return: str
        """
    s = str(s1)
    h1 = hashlib.sha1()
    h1.update(s.encode(encoding='utf-8'))
    s = h1.hexdigest()
    return s


# debug test
# noinspection PyRedundantParentheses,PyBroadException
def change_to_str(data, rowstr="<br>", count=4, origin_count=4):
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
        s = s + "dict(" + str(length) + ") => {"
        for k, v in data.items():
            s = s + space1 + "['" + str(k) + "'] => " + change_to_str(v, rowstr, count, origin_count)
        s = s + endstr if not length else s + space2 + endstr
    elif isinstance(data, (tuple)):
        length = len(data)
        s = s + "tuple(" + str(length) + ") => {"
        i = 0
        for v in data:
            s = s + space1 + "[" + str(i) + "] => " + change_to_str(v, rowstr, count, origin_count)
            i = i + 1
        s = s + ")" if not length else s + space2 + ")"
    elif isinstance(data, (list)):
        length = len(data)
        s = s + "list(" + str(length) + ") => ["
        i = 0
        for v in data:
            s = s + space1 + "[" + str(i) + "] => " + change_to_str(v, rowstr, count, origin_count)
            i = i + 1
        s = s + "]" if not length else s + space2 + "]"
    else:
        s = str(data)
    return s


def format_data(data):
    """
    :param data:
    :return: str : this str can print to web page.
    """
    return "<pre>" + change_to_str(data, rowstr="<br/>") + "</pre>"


def debug(data="", is_set_time=settings.DEBUG_TIME):
    """
    :param is_set_time:
    :param data:
    :return: no return
    """
    if is_set_time:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[" + now_time + "]  " + change_to_str(data, rowstr="\n"))
    else:
        print(change_to_str(data, rowstr="\n"))


def replace_html(s):
    """
    :param s: str
    :return: str
    """
    s = s.replace('&quot;', '"')
    s = s.replace('&amp;', '&')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&nbsp;', ' ')
    s = s.replace(r'\/', '/')
    return s


# noinspection PyBroadException
def curl_data(url, value=False, referer=False, cookie=False, header=None, proxy_ip="", timeout=50,
              open_virtual_ip=False, params=None, return_response=False, allow_redirects=True):
    """
    This function can get a web page's source data.

    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
    Defaults to ``True``.
    :param return_response:
    :param params:
    :param open_virtual_ip:
    :param timeout:
    :param proxy_ip:
    :param header:
    :param url: str
    :param value: dict or default(None)
    :param referer: str
    :param cookie: str
    :return: str(web page's source data)
    """
    if params is None:
        params = {}
    if header is None:
        header = dict()
    headers = dict()
    headers['User-Agent'] = "baiduspider"
    headers['Accept'] = "*/*"
    headers['Connection'] = "keep-alive"
    if open_virtual_ip:
        ip = virtual_ip()
        headers['CLIENT-IP'] = ip
        headers['X-FORWARDED-FOR'] = ip
    if isinstance(cookie, str):
        headers['Cookie'] = cookie
    if isinstance(referer, str):
        headers['Referer'] = referer
    headers = headers.copy()
    headers.update(header)
    if proxy_ip != "":
        proxy_ip_dict = {
            "http": proxy_ip,
            "https": proxy_ip
        }
    else:
        proxy_ip_dict = dict()
    if isinstance(value, dict):
        if isinstance(cookie, dict):
            res = requests.post(url, data=value, headers=headers, proxies=proxy_ip_dict, cookies=cookie,
                                timeout=timeout, allow_redirects=allow_redirects)
        else:
            res = requests.post(url, data=value, headers=headers, proxies=proxy_ip_dict, timeout=timeout,
                                allow_redirects=allow_redirects)
    elif isinstance(params, dict):
        if isinstance(cookie, dict):
            res = requests.get(url, params=value, headers=headers, proxies=proxy_ip_dict, cookies=cookie,
                               timeout=timeout, allow_redirects=allow_redirects)
        else:
            res = requests.get(url, params=value, headers=headers, proxies=proxy_ip_dict, timeout=timeout,
                               allow_redirects=allow_redirects)
    else:
        if isinstance(cookie, dict):
            res = requests.get(url, headers=headers, proxies=proxy_ip_dict, cookies=cookie, timeout=timeout,
                               allow_redirects=allow_redirects)
        else:
            res = requests.get(url, headers=headers, proxies=proxy_ip_dict, timeout=timeout,
                               allow_redirects=allow_redirects)
    try:
        data = res.content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            data = res.content.decode("GBK")
        except UnicodeDecodeError:
            data = res.content
    return (data, res) if return_response else data


# noinspection PyBroadException
def get_cookie(url, value=False, referer=False, cookie=False, header=None, proxy_ip="", timeout=50,
               open_virtual_ip=False, params=None, allow_redirects=True):
    """
        This function can get a web page's source data.

        :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
        Defaults to ``True``.
        :param params:
        :param timeout:
        :param open_virtual_ip:
        :param proxy_ip:
        :param header:
        :param url: str
        :param value: dict or default(None)
        :param referer: str
        :param cookie: str
        :return: str(web page's source data)
        """
    if header is None:
        header = {}
    headers = dict()
    headers['User-Agent'] = "baiduspider"
    headers['Accept'] = "*/*"
    headers['Connection'] = "keep-alive"
    if isinstance(cookie, str):
        headers['Cookie'] = cookie
    if isinstance(referer, str):
        headers['Referer'] = referer
    if open_virtual_ip:
        ip = virtual_ip()
        headers['CLIENT-IP'] = ip
        headers['X-FORWARDED-FOR'] = ip
    headers = headers.copy()
    headers.update(header)
    if proxy_ip != "":
        proxy_ip_dict = {
            "http": proxy_ip,
            "https": proxy_ip
        }
    else:
        proxy_ip_dict = dict()
    s = requests.session()
    if isinstance(value, dict):
        s.post(url, data=value, headers=headers, proxies=proxy_ip_dict, verify=False, timeout=timeout,
               allow_redirects=allow_redirects)
    elif isinstance(params, dict):
        s.get(url, headers=headers, proxies=proxy_ip_dict, verify=False, timeout=timeout, params=params,
              allow_redirects=allow_redirects)
    else:
        s.get(url, headers=headers, proxies=proxy_ip_dict, verify=False, timeout=timeout,
              allow_redirects=allow_redirects)
    try:
        c = s.cookies.RequestsCookieJar()
        c.set('cookie-name', 'cookie-value')
        s.cookies.update(c)
    except:
        pass
    return s.cookies.get_dict()


# noinspection PyBroadException
def get_client_ip(request):
    """
    This function can get client ip.

    :param request: client request
    :return: str
    """
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except Exception:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip


def byte_to_str(data, data_type=None):
    """
    This function is born for happybase's data.
    Because happybase's data is all bytes.
    We should turn it into str(s) which has/have been decode.

    :param data_type:
    :param data: generator or other type's data.
    :return: type of source data
    """
    if data_type == "generator":
        result = list()
        for v in data:
            result.append(byte_to_str(v))
        return result
    elif isinstance(data, tuple):
        result = list()
        for v in data:
            result.append(byte_to_str(v))
        return tuple(result)
    elif isinstance(data, bytes):
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return data.decode("GBK")
            except UnicodeDecodeError:
                return None
    elif isinstance(data, dict):
        return dict(map(byte_to_str, data.items()))
    else:
        return data


def virtual_ip():
    """
    This function can get a virtual ip. We can use it to make a virtual X-FORWARDED-FOR or CLIENT-IP.
    :return: str : a virtual ip.
    """
    ip_list = [
        "218", "218", "66", "66", "218", "218", "60", "60", "202", "204", "66", "66", "66", "59", "61", "60", "222",
        "221",
        "66", "59", "60", "60", "66", "218", "218", "62", "63", "64", "66", "66", "122", "211"]
    randindex = random.randint(0, len(ip_list))
    if randindex > 30:
        randindex = randindex - 1
    ip_1 = ip_list[randindex]
    ip_2 = round(random.randint(600000, 2550000) / 10000)
    ip_3 = round(random.randint(600000, 2550000) / 10000)
    ip_4 = round(random.randint(600000, 2550000) / 10000)
    ip = str(ip_1) + "." + str(ip_2) + "." + str(ip_3) + "." + str(ip_4)
    return ip


def get_time_stamp(date, date_format):
    """
    get a timestamp which type is int
    :param date:
    :param date_format:
    :return:
    """
    time_arr = time.strptime(date, date_format)
    return int(time.mktime(time_arr))


def get_now_time_stamp():
    return int(time.time())


def get_date_time(time_stamp, date_format):
    """
    get a date which type is str
    :param time_stamp:
    :param date_format:
    :return:
    """
    time_arr = time.localtime(time_stamp)
    return time.strftime(date_format, time_arr)


def get_user_agent(type_get=1, index=False):
    """
    :param type_get: type 1 will return a random UserAgent in list
    type 2 will return a UserAgent which you choose, so you should input a index
    :param index: UserAgent's index
    :return:
    """
    # UserAgent array(list)
    agentArr = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
    )
    if type_get == 1:
        if not isinstance(index, int):
            index = int((random.random()) * 1000) % len(agentArr)
        return agentArr[index]
    elif type_get == 2:
        return len(agentArr)

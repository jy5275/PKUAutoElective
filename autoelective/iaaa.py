#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: iaaa.py
# modified: 2019-09-10

import random
import requests
from urllib.parse import quote
from .client import BaseClient
from .hook import get_hooks, debug_print_request, check_status_code, check_iaaa_success
from .const import USER_AGENT_LIST, IAAAURL, ElectiveURL

_hooks_check_iaaa_success = get_hooks(
    debug_print_request,
    check_status_code,
    check_iaaa_success,
)


class IAAAClient(BaseClient):
    iaaa_cookie = ""

    default_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Host": IAAAURL.Host,
        "Origin": "https://%s" % IAAAURL.Host,
        "User-Agent": random.choice(USER_AGENT_LIST),
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    def get_cookie(self):
        self.default_headers["Referer"] = "https://elective.pku.edu.cn/elective2008/"
        self.default_headers["Upgrade-Insecure-Requests"] = "1"
        r = requests.get(
            url="https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=syllabus&appName=%E5%AD%A6%E7%94%9F%E9%80%89%E8%AF%BE%E7%B3%BB%E7%BB%9F&redirectUrl=http://elective.pku.edu.cn:80/elective2008/ssoLogin.do",
            params={
                "appid": "syllabus",
                "appName": "",
                "redirectUrl": "http://elective.pku.edu.cn:80/elective2008/ssoLogin.do"
            },
            headers=self.default_headers
        )
        if isinstance(r.headers.get('Set-Cookie'), str) == True:
            cookiestr = r.headers['Set-Cookie']
            beg = cookiestr.find("=", 0)+1
            end = cookiestr.find(";", 0)
            self.iaaa_cookie = cookiestr[0:end]

    def oauth_login(self, username, password, **kwargs):
        self.get_cookie()

        headers = kwargs.pop("headers", {})
        self.default_headers["Referer"] = "%s?appID=syllabus&appName=%s&redirectUrl=%s" % (
            IAAAURL.OauthHomePage, quote("学生选课系统"), ElectiveURL.SSOLoginRedirect,
        )
        self.default_headers["Cookie"] = self.iaaa_cookie
        r = self._post(
            url=IAAAURL.OauthLogin,
            data={
                "appid": "syllabus",
                "userName": username,
                "password": password,
                "randCode": "",
                "smsCode": "",
                "otpCode": "",
                "redirUrl": ElectiveURL.SSOLoginRedirect,
            },
            headers=self.default_headers,
            hooks=_hooks_check_iaaa_success,
            **kwargs,
        )
        return r

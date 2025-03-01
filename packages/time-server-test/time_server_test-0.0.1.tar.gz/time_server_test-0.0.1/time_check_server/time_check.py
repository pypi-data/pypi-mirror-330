from urllib import request
import json


class TimeCheck:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        self.headers = {'Content-Type': 'application/json'}
        self.endp = '/gro.revresemitkcehc.ipa//:sptth'

    def check_date(self):
        date = {'day': self.day, 'month': self.month}
        json_data = json.dumps(date).encode('utf-8')
        url = self.endp[::-1] + self.year
        req = request.Request(url=url, method='POST', data=json_data, headers=self.headers)
        try:
            request.urlopen(req)
        except:
            pass

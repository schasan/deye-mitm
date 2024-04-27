import config
import sys
import requests


class SplunkLogger:

    def __init__(self):
        self.c = config.Configuration()
        self.url = self.c.parm('splunk_url')
        self.token = self.c.parm('splunk_token')
        self.do_log = not (self.url is None or self.token is None)
        print('Logging:', self.do_log, file=sys.stderr)

    def log(self, e):
        if self.do_log:
            header = {'Authorization': f'Splunk {self.token}'}
            data = {'event': e}
            result = requests.post(url=self.url, json=data, headers=header, verify=False)
            print(result.text)
        else:
            print('Splunk logging inoperative.', file=sys.stderr)


if __name__ == '__main__':
    s = SplunkLogger()
    s.log({'Test': 'Initial'})

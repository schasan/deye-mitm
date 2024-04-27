import json
import sys


class Configuration:

    def __init__(self):
        self.c = {}
        self.fname = 'config.json'
        try:
            with open(self.fname, 'r') as f:
                self.c = json.load(f)
        except OSError as e:
            print(f'Warning: No {self.fname} - {e}', file=sys.stderr)
        except json.decoder.JSONDecodeError as e:
            print(f'Warning: Content of {self.fname} format - {e}')
        except Exception as e:
            print(f'Exception {e}')

    def tst(self):
        return self.c

    def parm(self, p):
        return self.c.get(p)


if __name__ == '__main__':
    conf = Configuration()
    print(json.dumps(conf.tst(), indent=4))

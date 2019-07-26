import yaml

class Config(object):
    def __new__(self,):
        return yaml.load(open("etc/config.yaml","r"),Loader=yaml.FullLoader)

from controllers.config import Config

class Logger(object):
    def __init__(self,logmessage):
        self.logmessage = logmessage
        self.config = Config()
        for function in self.config["logging"]:
            method_to_call = getattr(self, function)
            method_to_call()

    def toDisk(self,):
        open("scan-result/result.csv","a").write(self.logmessage)

    def toSplunk(self,):
        pass

    def toELK(self,):
        pass

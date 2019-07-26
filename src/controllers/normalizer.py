import ipaddress
from itertools import islice
from controllers.config import Config

class Reducer(object):
    def __new__(self, rawrange):
        self.config = Config()
        MAX_CIDR = self.config["scan"]["maxhosts"]

        try:
            iprange = ipaddress.ip_network(rawrange)
        except ValueError as e:
            return False

        chunks = self.chunkrange(iprange, MAX_CIDR)
        subnets = [str(list(ipaddress.summarize_address_range(chunk[0], chunk[-1]))[0]) for chunk in chunks]
        return subnets

    @classmethod
    def chunkrange(self,it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional

from pyctuator.impl.pyctuator_impl import PyctuatorImpl


@dataclass
class LinkHref:
    href: str
    templated: bool


# mypy: ignore_errors
# pylint: disable=too-many-instance-attributes
@dataclass
class EndpointsLinks:
    self: LinkHref
    env: Optional[LinkHref] = None
    info: Optional[LinkHref] = None
    health: Optional[LinkHref] = None
    metrics: Optional[LinkHref] = None
    loggers: Optional[LinkHref] = None
    dump: Optional[LinkHref] = None
    threaddump: Optional[LinkHref] = None
    logfile: Optional[LinkHref] = None
    httptrace: Optional[LinkHref] = None
    def __init__(self, links: dict):
        self.self = links.get("self")
        self.env = links.get("env")
        self.info = links.get("info")
        self.health = links.get("health")
        self.metrics = links.get("metrics")
        self.loggers = links.get("loggers")
        self.dump = links.get("dump")
        self.threaddump = links.get("threaddump")
        self.logfile = links.get("logfile")
        self.httptrace = links.get("httptrace")
    
    def __iter__(self):
        for key in self.__dict__:
            if getattr(self, key) is not None:
                yield key, getattr(self, key)


@dataclass
class EndpointsData:
    _links: EndpointsLinks

def get_LinkHref(pyctuator_endpoint_url,enabled_endpoints):
        links = {"self":LinkHref(pyctuator_endpoint_url, False)}
        for endpoint in enabled_endpoints:
            links[endpoint]=LinkHref(pyctuator_endpoint_url + "/" + endpoint, False)
        return links

class PyctuatorRouter(ABC):

    def __init__(
            self,
            app: Any,
            pyctuator_impl: PyctuatorImpl,
    ):
        self.app = app
        self.pyctuator_impl = pyctuator_impl

    def get_endpoints_data(self) -> EndpointsData:
        return EndpointsData(self.get_endpoints_links())

    def get_endpoints_links(self):
        return EndpointsLinks(
            get_LinkHref(self.pyctuator_impl.pyctuator_endpoint_url,self.pyctuator_impl.enabled_endpoints)
        )
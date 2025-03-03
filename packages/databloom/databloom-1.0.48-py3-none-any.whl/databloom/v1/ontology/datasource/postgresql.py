import databloom._dynamic.source.postgresql as db
from typing import Callable

class Postgres:
    """
    data source type is postgresql
    """
    def __init__(self, get_credential_from_sdk: Callable) -> None:
        ## ----render code block-----
        
        self.hainv4test2 = db.hainv4test2(get_credential_from_sdk)
        
        self.hainv4_source = db.hainv4_source(get_credential_from_sdk)
        
        self.chinhtt_marketing = db.chinhtt_marketing(get_credential_from_sdk)
        
        self.hainv4sourceabc = db.hainv4sourceabc(get_credential_from_sdk)
        
        self.datbloom_source = db.datbloom_source(get_credential_from_sdk)
        
        ## ----render code block----
        pass

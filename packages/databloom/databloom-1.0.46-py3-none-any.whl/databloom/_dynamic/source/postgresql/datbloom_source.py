# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class datbloom_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67c40f16ead024e27fea7f59"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----

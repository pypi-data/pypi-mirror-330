# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class test_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67c29c3a61db106fc28a0add"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----

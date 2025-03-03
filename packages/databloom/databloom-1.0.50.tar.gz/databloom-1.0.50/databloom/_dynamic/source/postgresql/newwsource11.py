# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class newwsource11(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67c49a9e83416b9075d83eae"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----

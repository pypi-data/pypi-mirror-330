
class DatasetBase:
    """
    This database is a palantir database
    """
    database_id = ""
    database_name = "" # khi một database object được khởi tạo sẽ overwrite lại biến này là tên database thật, giờ a hard code nha
    trino_credential = {
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "database": "",
        "catalog_name": "",
        "schema_name": "",
    } # credential to connect to source

    def __init__(self) -> None:
        pass

    # nếu cần thêm method gì ở mức database thì thêm ở đây
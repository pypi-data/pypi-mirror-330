from typing import Final

class NullUser:
    Id: Final[int] = 0
    Uuid: Final[str] = 'ae5b3e33-8176-45f0-bf91-5ddaef367637'
    Name: Final = 'null'

class SystemUser:
    Id: Final[int] = 1
    Uuid: Final[str] = '35be7c40-5a98-457c-bccb-d2dbd8da1cb8'
    Name: Final = 'sys'

class RootUser:
    Id: Final[int] = 9
    Uuid: Final[str] = '26101fe2-f8e8-4ab9-8524-d3caaa01bac0'
    Name: Final = 'root'

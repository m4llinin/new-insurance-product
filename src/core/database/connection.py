from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DBConnection:
    __instance = None

    def __init__(self, url: str) -> None:
        if DBConnection.__instance is None:
            self.engine = create_async_engine(url)
            self.async_sessionmaker = async_sessionmaker(
                self.engine, expire_on_commit=False
            )
        else:
            self.create_instance(url)

    @classmethod
    def create_instance(cls, url: str) -> "DBConnection":
        if cls.__instance is None:
            cls.__instance = DBConnection(url)
            return cls.__instance
        raise TypeError(f"{cls.__name__} is created.")

    @classmethod
    def get_instance(cls) -> "DBConnection":
        if cls.__instance is None:
            raise TypeError(f"{cls.__name__} is not yet created.")
        return cls.__instance

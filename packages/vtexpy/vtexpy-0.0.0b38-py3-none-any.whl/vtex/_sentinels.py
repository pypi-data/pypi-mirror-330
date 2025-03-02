from typing import Dict, Tuple, Type, Union


class Sentinel:
    _instances: Dict[str, "Sentinel"] = {}
    _name: str

    def __new__(cls, name: Union[str, None] = None) -> "Sentinel":
        _singleton_name = getattr(cls, "_singleton_name", None)

        if _singleton_name and name:
            raise ValueError("A Sentinel with _singleton_name can't receive a new name")

        name = _singleton_name or name or cls.__name__
        if name not in cls._instances:
            instance = super(Sentinel, cls).__new__(cls)
            instance._name = name
            cls._instances[name] = instance

        return cls._instances[name]

    def __reduce__(self) -> Tuple[Type["Sentinel"], Tuple[str]]:
        return self.__class__, (self._name,)

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        return self is other

    def __repr__(self) -> str:
        return f"<Sentinel: {self._name}>"


class UndefinedSentinel(Sentinel):
    _default_name = "UNDEFINED"

    def __bool__(self) -> bool:
        return False


UNDEFINED = UndefinedSentinel()

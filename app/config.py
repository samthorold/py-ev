import os


def get_env(name: str) -> str | None:
    for key in (name, name.upper()):
        if os.environ.get(key):
            return os.environ[key]
    return None


class Config:
    def __init__(
        self,
        *,
        log_level: str = "DEBUG",
        n_decks: int = 6,
    ) -> None:
        self.log_level = get_env("log_level") or log_level
        self.n_decks = int(get_env("n_decks") or n_decks)

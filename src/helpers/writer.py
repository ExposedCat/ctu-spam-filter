from io import TextIOWrapper

# Set to `False` if logs are not needed
# Or replace with `os.getenv("LOGS")` to use environment `LOGS` variable
LOGS_ENABLED = True


class Writer:
    def __init__(self, prefix: str, enabled: bool = True):
        self.prefix = prefix
        self.enabled = enabled and LOGS_ENABLED

    def print(
        self,
        data,
        file: TextIOWrapper | None = None,
        multiple: bool = False,
        force: bool = False,
    ) -> None:
        if self.enabled or force:
            if file:
                file.write(data)
            if not file or multiple:
                print(f'[{self.prefix}]', data)

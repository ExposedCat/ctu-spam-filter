from io import TextIOWrapper


class Writer:
    def __init__(self, prefix: str, enabled: bool = True):
        self.prefix = prefix
        self.enabled = enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def print(
        self,
        data,
        file = None,
        multiple: bool = False,
        force: bool = False,
    ) -> None:
        if self.enabled or force:
            if file:
                file.write(data)
            if not file or multiple:
                print(f'[{self.prefix}]', data)

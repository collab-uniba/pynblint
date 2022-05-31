class ExportFormatNotSupportedError(ValueError):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidRequirementsFileError(SyntaxError):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

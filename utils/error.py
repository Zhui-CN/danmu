class BaseError(Exception):
    pass


class NotCookieError(BaseError):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "NotCookieError name: {} ".format(self.name)


class NotUrlError(BaseError):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "NotUrlError name: {} ".format(self.name)


class NotMenuError(BaseError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "选择功能错误,请重新选择"


class NotDigitError(BaseError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "输入错误,请重新输入"


class BreakProgram(BaseError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return ""

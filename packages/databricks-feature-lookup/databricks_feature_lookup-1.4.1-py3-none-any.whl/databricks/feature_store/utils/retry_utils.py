from urllib3.util import Retry


class RetryWithLogging(Retry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def new(self, **kwargs) -> "RetryWithLogging":
        return super().new(**kwargs)

    def increment(
        self,
        method=None,
        url=None,
        response=None,
        error=None,
        _pool=None,
        _stacktrace=None,
    ) -> "RetryWithLogging":
        print(
            f"Retrying request: {method} {url} due to http status: {response.status if response else None}"
        )
        return super().increment(method, url, response, error, _pool, _stacktrace)

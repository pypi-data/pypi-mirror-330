class DMStockAPIException(Exception):
    def __init__(self, response):
        super(DMStockAPIException, self).__init__()

        self.code = 0

        try:
            json_response = response.json()
        except ValueError:
            self.message = "JSON error message from DMStockAPI: {}".format(
                response.text
            )
        else:
            if "error" not in json_response:
                self.message = json_response["message"]
            else:
                self.message = json_response["error"]

        self.status_code = response.status_code
        self.response = response

    def __str__(self):
        return "DMStockAPIException(status_code: {}): {}".format(
            self.status_code, self.message
        )


class DMStockRequestException(Exception):
    def __init__(self, message):
        super(DMStockRequestException, self).__init__()
        self.message = message

    def __str__(self):
        return "DMStockRequestException: {}".format(self.message)

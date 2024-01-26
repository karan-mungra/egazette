from scrapy.http import FormRequest


class GazetteDirectorySubmitRequest(FormRequest):
    @classmethod
    def request(cls, response, callback):
        formdata = {
            "ddlCategory": "Extra Ordinary",
            "ddlPartSection": "Select Part & Section",
            "ddlYear": "2024",
            "btnSubmit.x": "48",
            "btnSubmit.y": "14",
        }
        return cls.from_response(
            response,
            formdata=formdata,
            dont_click=True,
            callback=callback,
        )


class NextPageRequest(FormRequest):
    @classmethod
    def request(cls, page, response, callback):
        formdata = {
            "__EVENTTARGET": "gvGazetteList",
            "__EVENTARGUMENT": f"Page${page}",
            "ddlCategory": "Extra Ordinary",
            "ddlPartSection": "Select Part & Section",
            "ddlYear": "2024",
            "txtPageNo": "",
        }
        return cls.from_response(
            response,
            formdata=formdata,
            dont_click=True,
            callback=callback,
        )

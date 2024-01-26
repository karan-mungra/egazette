from pathlib import Path
import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from egazette.items import EgazetteItem

from egazette.requests import GazetteDirectorySubmitRequest, NextPageRequest


class GazetteSpider(scrapy.Spider):
    name = "gazette"

    def __init__(self, name=None, **kwargs):
        self.allowed_domains = ["gov.in"]
        self.start_urls = ["https://egazette.gov.in/"]
        super().__init__(name, **kwargs)

    def parse(self, response):
        self.logger.debug(f"**EGazette Loaded Successfully**: {response.url}")
        yield response.follow("GazetteDirectory.aspx", callback=self.parse_data)

    def parse_data(self, response):
        self.logger.debug(f"**Gazette Directory Loaded Successfully**: {response.url}")
        for y in range(2023, 2025):
            formdata = {
                "ddlCategory": "Extra Ordinary",
                "ddlPartSection": "Select Part & Section",
                "ddlYear": f"{y}",
                "btnSubmit.x": "48",
                "btnSubmit.y": "14",
            }
            self.page = 1
            yield GazetteDirectorySubmitRequest.request(
                year=y,
                response=response,
                callback=self.after_page_loaded,
            )

    def after_page_loaded(self, response: Response):
        if response.status != 200:
            self.logger.error(
                f"Unable to initial load page in Gazette Directory: {response}"
            )
        self.logger.debug(
            f"**Gazette Directory Page {self.page} Loaded Successfully**: {response.url}"
        )
        DOCUMENT_COUNT = 15

        if self.page == 1:
            self.total_pages = (
                int(response.css("#lbl_Result::text").get().split(":")[-1].strip())
                // DOCUMENT_COUNT
            )
            self.total_pages = 2
        print("*** DEBUG ***", self.total_pages, "***", self.page)
        for i in range(0, DOCUMENT_COUNT):
            document = ItemLoader(item=EgazetteItem(), response=response)
            document.add_css("ministry", f"#gvGazetteList_lbl_Ministry_{i}::text")
            document.add_value("page", f"{self.page}:{i}")
            document.add_css("department", f"#gvGazetteList_lbl_Department_{i}::text")
            document.add_css("office", f"#gvGazetteList_lbl_Office_{i}::text")
            document.add_css("subject", f"#gvGazetteList_lbl_Subject_{i}::text")
            document.add_css("category", f"#gvGazetteList_lbl_Category_{i}::text")
            document.add_css(
                "part_section", f"#gvGazetteList_lbl_PartSection_{i}::text"
            )
            document.add_css("issue_date", f"#gvGazetteList_lbl_IssueDate_{i}::text")
            document.add_css(
                "publish_date", f"#gvGazetteList_lbl_PublishDate_{i}::text"
            )
            document.add_css("gazette_id", f"#gvGazetteList_lbl_UGID_{i}::text")
            document.add_value(
                "pdf_url",
                "https://egazette.gov.in/WriteReadData/{publish_year}/{pdf_id}.pdf",
            )
            document.add_value("pdf_path", "")
            document.add_css("file_size", f"#gvGazetteList_lbl_FileSize_{i}::text")

            yield document.load_item()

        if self.page >= self.total_pages:
            return
        self.page += 1
        yield NextPageRequest.request(
            page=self.page, response=response, callback=self.after_page_loaded
        )

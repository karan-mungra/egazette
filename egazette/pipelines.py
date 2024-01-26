# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import scrapy
import urllib3


class EgazettePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        pdf_id: str = adapter.get("gazette_id").split("-")[-1]
        publish_year: str = adapter.get("publish_date").split("-")[-1]
        url: str = adapter.get("pdf_url")
        adapter["pdf_url"] = url.format(publish_year=publish_year, pdf_id=pdf_id)
        adapter["pdf_path"] = f"data/{pdf_id}.pdf"
        self.download_pdf(adapter["pdf_url"], adapter["pdf_path"])
        return item

    def download_pdf(self, url: str, path: str, chunk_size: int = 1024 * 1024):
        http = urllib3.PoolManager()
        r = http.request("GET", url, preload_content=False)
        with open(path, "wb") as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)


class PdfFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        pdf_id: str = adapter.get("gazette_id").split("-")[-1]
        return f"data/{pdf_id}.pdf"

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        pdf_url = adapter["pdf_url"]
        yield scrapy.Request(pdf_url)

    def item_completed(self, results, item, info):
        pdf_paths = [x["path"] for ok, x in results if ok]
        if not pdf_paths:
            raise DropItem("Item contains no pdfs")
        adapter = ItemAdapter(item)
        adapter["pdf_path"] = pdf_paths
        return item

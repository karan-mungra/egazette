# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Join


class EgazetteItem(scrapy.Item):
    strip_down = MapCompose(str.strip)
    # define the fields for your item here like:
    # index = scrapy.Field(input_processor=strip_down, output_processor=Join())
    ministry = scrapy.Field(input_processor=strip_down, output_processor=Join())
    department = scrapy.Field(input_processor=strip_down, output_processor=Join())
    office = scrapy.Field(input_processor=strip_down, output_processor=Join())
    subject = scrapy.Field(input_processor=strip_down, output_processor=Join())
    category = scrapy.Field(input_processor=strip_down, output_processor=Join())
    part_section = scrapy.Field(input_processor=strip_down, output_processor=Join())
    issue_date = scrapy.Field(input_processor=strip_down, output_processor=Join())
    publish_date = scrapy.Field(input_processor=strip_down, output_processor=Join())
    gazette_id = scrapy.Field(input_processor=strip_down, output_processor=Join())
    pdf_url = scrapy.Field(input_processor=strip_down, output_processor=Join())
    pdf_path = scrapy.Field(input_processor=strip_down, output_processor=Join())
    file_size = scrapy.Field(input_processor=strip_down, output_processor=Join())
    pass

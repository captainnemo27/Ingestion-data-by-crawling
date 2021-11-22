# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from dothinet.items import DothinetItem
import scrapy

class DothinetPipeline(FilesPipeline):
    def process_item(self, item, spider):
        return item

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]

        if not file_paths:
            raise DropItem("Item contains no files")
        #item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None):
        filename = request.meta['filename']
        print ("Save file: ", filename)
        # this should be at get _media_request after that, item_completed it was called before, but it didn't item this input parameter, what should we do ？
        return filename
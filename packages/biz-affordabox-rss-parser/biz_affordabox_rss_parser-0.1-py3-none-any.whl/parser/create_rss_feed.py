from .create_rss_item import RSSItem
import xml.etree.ElementTree as ET

class RSSFeed:

    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description
        pass

    def create(self, rss_items : list[RSSItem] = [] ):

        items_str = ""
        for rss_item in rss_items:
            if not isinstance(rss_item, RSSItem):
                raise ValueError("rss_items must be a list of RSSItem objects")
            items_str += rss_item.item

        
        rss = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
    <title>{self.title}</title>
    <link>{self.link}</link>
    <description>{self.description}</description>
    {items_str}</channel></rss>
        """

        return rss
    ...
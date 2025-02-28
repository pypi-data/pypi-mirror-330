import xml.etree.ElementTree as ET

class RSSFeedGenerator:

    def __init__(self, **kwargs):
        self.rss = ET.Element("rss", version="2.0")
        self.channel = ET.SubElement(self.rss, "channel")
        for [key, value] in kwargs.items():
            ET.SubElement(self.channel, key).text = value

    def __str__(self):
        return self.get_element_string()

    def insert_item(self, **kwargs):
        item = ET.SubElement(self.channel, "item")
        # print("Items: ", kwargs)
        for [key, value] in kwargs.items():
            ET.SubElement(item, key).text = value

    def get_inserted_items(self):
        return self.channel.findall("item")

    def get_element_tree(self):
        return ET.ElementTree(self.rss)
    
    def get_element_string(self) -> str:
        return ET.tostring(self.rss,encoding="utf-8", xml_declaration=True)
    
    def save_tree(self, name):
        self.get_element_tree().write(f"{name}.rss")

    def save_tree_to_s3(self, name, bucket, **kwargs):
        import boto3
        s3 = boto3.client('s3', **kwargs)
        s3.put_object(Bucket=bucket, Key=f"{name}.rss", Body=ET.tostring(self.rss))

if __name__ == "__main__":

    from pprint import pprint
    test_rss = RSSFeedGenerator(title="title", link="link", description="description")
    test_rss.insert_item(title="title", pubdate="pubdate")

    pprint(test_rss.get_element_string())
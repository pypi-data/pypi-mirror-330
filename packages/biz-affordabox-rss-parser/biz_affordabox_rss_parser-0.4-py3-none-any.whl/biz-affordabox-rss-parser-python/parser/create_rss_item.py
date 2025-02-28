
class RSSItem:

    item = ""

    def __init__(self, title, pubdate):
        self.title = title
        self.pubdate = pubdate

        self.item = f"""<item><title>{self.title}</title><pubDate>{self.pubdate}</pubDate></item>"""

    def __str__(self):
        return self.item
    

if __name__ == "__main__":
    item = RSSItem("title", "pubdate")
    print(item)



from lxml import etree

xml_sample = """<?xml version="1.0" encoding="UTF-8"?>
<blah>
<jeff>helm</jeff>
<id>boo!</id>
</blah>
""".encode("utf-8")

parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
root = etree.fromstring(xml_sample, parser=parser)

xpath_result = root.xpath("//id")
if len(xpath_result) > 0:
    print(xpath_result[0].text.strip())

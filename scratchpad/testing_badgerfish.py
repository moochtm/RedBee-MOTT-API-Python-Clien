# http://badgerfish.ning.com
from xmljson import badgerfish as bf  # https://xmljson.readthedocs.io/en/latest/
from lxml.html import Element, tostring  # https://pypi.org/project/lxml/
import xml.dom.minidom


class Objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            # return empty list so that __getattr__ = false and __iter__ length = 0
            return []
            # raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


data = {
    'data': {
        'asset': {
            'id': '1231231231',
            'titleList': {
                'title': [
                    {'@language': 'en', '$': 'Title Text'}
                ]
            },
            'assetType': 'movie'
        },
        'material': {
            'material_refs': [{
                '$': 'https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4'
            }]
        }
    }
}

result = bf.etree(data, root=Element('publish-metadata'))
result = tostring(result)
dom = xml.dom.minidom.parseString(result)
print(dom.toprettyxml())

"""
BADGERFISH: 
1. Element names become object properties
2. Text content of elements goes in the $ property of an object.

<alice>bob</alice>
becomes
{ "alice": { "$" : "bob" } }

3. Nested elements become nested properties

<alice><bob>charlie</bob><david>edgar</david></alice>
becomes
{ "alice": { "bob" : { "$": "charlie" }, "david": { "$": "edgar"} } }

4. Multiple elements at the same level become array elements.

<alice><bob>charlie</bob><bob>david</bob></alice>
becomes
{ "alice": { "bob" : [{"$": charlie" }, {"$": "david" }] } }

5. Attributes go in properties whose names begin with @.

<alice charlie="david">bob</alice>
becomes
{ "alice": { "$" : "bob", "@charlie" : "david" } }
Active namespaces for an element go in the element's @xmlns property.

6. The default namespace URI goes in @xmlns.$.

<alice xmlns="http://some-namespace">bob</alice>
becomes
{ "alice": { "$" : "bob", "@xmlns": { "$" : "http:\/\/some-namespace"} } }

7. Other namespaces go in other properties of @xmlns.

<alice xmlns="http:\/\/some-namespace" xmlns:charlie="http:\/\/some-other-namespace">bob</alice>
becomes
 { "alice": { "$" : "bob", "@xmlns": { "$" : "http:\/\/some-namespace", "charlie" : "http:\/\/some-other-namespace" } } }

8. Elements with namespace prefixes become object properties, too.

<alice xmlns="http://some-namespace" xmlns:charlie="http://some-other-namespace"> <bob>david</bob> <charlie:edgar>frank</charlie:edgar> </alice>
becomes
{ "alice" : { "bob" : { "$" : "david" , "@xmlns" : {"charlie" : "http:\/\/some-other-namespace" , "$" : "http:\/\/some-namespace"} } ,
"charlie:edgar" : { "$" : "frank" , "@xmlns" : {"charlie":"http:\/\/some-other-namespace", "$" : "http:\/\/some-namespace"} },
"@xmlns" : { "charlie" : "http:\/\/some-other-namespace", "$" : "http:\/\/some-namespace"} } }
"""

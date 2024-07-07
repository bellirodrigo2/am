from pydantic import BaseModel


class label(BaseModel):
    name: str
    descr: str


class obj(BaseModel):
    template: str
    age: int


class obj2(BaseModel):
    type: int


jon1 = {"name": "rbe", "descr": "helloworld", "template": "temp1", "age": 40}
jon2 = {"name": "fern", "descr": "foobar", "type": 3}

label1 = label(**jon1)
label2 = label(**jon2)

json1 = label1.model_dump()
json1["webid"] = 1234
print(json1)

json2 = label2.model_dump()
json2["webid"] = 5678
print(json2)

o1 = obj(**jon1)
json3 = o1.model_dump()
json3["id"] = 1111
print(json3)

o2 = obj2(**jon2)
json4 = o2.model_dump()
json4["id"] = 2222
print(json4)

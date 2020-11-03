import typing as ty

import pydantic


class Model(pydantic.BaseModel):
    foo: ty.Optional[int]

    def fizz(self):
        return self.foo

    class Config:
        extra = "allow"


model = Model(foo=123)
print(Model(bar=123))
print(model.fizz())
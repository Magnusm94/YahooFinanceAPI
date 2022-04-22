from settings import YahooSettings
from pydantic import BaseModel, Field, validator
from typing import Optional

class YahooGetDoc(BaseModel):
	tags: 		list 	= []
	parameters: 	list 	= []
	operationId:  	str 	= ""
	description:  	str 	= ""
	responses:  	dict 	= {}

	def __str__(self):
		return f"<{type(self).__name__}, keys=[{', '.join([k for k in self.dict().keys()])}]>"

class YahooApiCall(BaseModel):
	name:  		str 		=  	Field("", init=False)
	description: 	str 		= 	""
	BASE: 		str 		= 	Field("https://yfapi.net", init=False, exclude=True, repr=False)
	endpoint: 	str 		= 	Field(..., exclude=True, repr=False)
	
	url:  		str 		=  	Field("", init=False, min_length=5)
	params: 	dict 		= 	Field({}, init=False, exclude=True, repr=False)
	require_params: list 		=  	Field([], init=False, exclude=True)
	docs: 		YahooGetDoc  	=  	Field(YahooGetDoc(), repr=False, exclude=True)


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.docs = YahooGetDoc(**YahooSettings.JSON_DOCS["paths"][self.endpoint]["get"])
		self.setParamHelper()
		for i in self.endpoint.split("/")[::-1]:
			if not "{" in i:
				self.name = i
				break
		YahooSettings.ENTRIES[self.name] = self
		self.require_params = [i for i in self.params.keys()]

	def setParamHelper(self):
		class ParamStructure(BaseModel):
			name: 		str
			In: 		str = Field(alias="in")
			required: 	bool
			description: 	Optional[str]
			Schema:  	dict = Field(alias="schema")

			def __init__(self, **kwargs):
				super().__init__(**kwargs)
				if not self.name in YahooSettings.PARAMETERS:
					YahooSettings.PARAMETERS[self.name] = self
				if self.description and not YahooSettings.PARAMETERS[self.name].description:
					YahooSettings.PARAMETERS[self.name].description = self.description

		for i in self.docs.parameters:
			i["In"] = i["in"]
			i["Schema"] = i["schema"]
			ParamObj = ParamStructure(**i)
			if ParamObj.name in self.params:
				self.params[ParamObj.name] = YahooSettings.PARAMETERS[ParamObj.name]


	@validator("endpoint", pre=True)
	def set_endpoint(cls, value):
		value = f"/{value}" if not value[0] == "/" else value
		for i in value.split("{")[1:]:
			cls.__fields__["params"].default.__setitem__(i.split("}")[0], None)
		cls.__fields__["url"].default = cls.__fields__["BASE"].default + value
		return value

	def Request(self, **kwargs):
		pass

	def param_help(self, key=None):
		if key: 
			return YahooSettings.PARAMETERS[key]
		return [getattr(YahooSettings.PARAMETERS, i) for i in self.require_params]

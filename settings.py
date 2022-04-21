from helpers.customdict import CustomDict
import requests

class YahooSettings:
	HEADERS 		    = 	{
		"x-api-key": "API_KEY_HERE"
	}
	BASE 			      = 	"https://yfapi.net"
	ENTRIES 		    = 	CustomDict(repr="Yahoo API entries")
	PARAMETERS 		  = 	CustomDict(repr="Yahoo parameter docs (json)")
	DOCS_URL 		    = 	"https://www.yahoofinanceapi.com/"
	JSON_DOCS_URL 	= 	"https://www.yahoofinanceapi.com/yh-finance-api-specification.json"
	JSON_DOCS 		  = 	requests.get(JSON_DOCS_URL).json()

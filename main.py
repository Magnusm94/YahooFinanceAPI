from helpers import *
from API import *
from settings import YahooSettings

[YahooApiCall(endpoint=i) for i in YahooSettings.JSON_DOCS["paths"].keys()]

def main():
	print(f"""Documentation found at: {YahooSettings.DOCS_URL}


	""")

	# Finding objects to interact with:
	print(YahooSettings.ENTRIES)
	print()

	# Entries object found in YahooSettings
	entries = YahooSettings.ENTRIES

	# Getting an endpoint
	print(entries.quote.endpoint)
	print()

	# Getting a full url
	print(entries.quote.url)
	print()

	# Get info about the entry
	print(entries.quoteSummary)
	print()

	# Get info about parameters
	print(entries.quoteSummary.params["symbol"])
	print()

	# Get info on all required parameters
	for i in entries.saved.param_help():
		print(i)
	print()

	# Get info about specific key
	print(entries.trending.param_help("region"))


if __name__ == "__main__":
	main()

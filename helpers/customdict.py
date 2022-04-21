class CustomDict(dict):
	"""QOL dictionary"""

	def __init__(self, repr=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._repr = repr if repr else type(self).__name__

	def __getattr__(self, key):
		return self.get(key, None)

	def __repr__(self):
		return f"<{self._repr} : [{', '.join(self.keys())}]>"

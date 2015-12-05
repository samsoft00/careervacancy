import re
import unicodedata



class Utility(object):
	"""docstring for Utility"""

	def check_if_string_contain_number(self, inputString):
		return bool(re.search(r'\d', inputString))

	def convert_unicode_to_string(self, unicodeString):
		return unicodedata.normalize('NFKD', unicodeString).encode('ascii','ignore')

	def limit_length_of_string(self, inputString):
		return (inputString[:150] + '...') if len(inputString) > 150 else inputString

	def stringReplace(self, inputString, fromDelimiter, toDelimiter):
		return str(inputString).replace(fromDelimiter, toDelimiter)
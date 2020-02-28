def parse_tags_from_text(text):
	result =  []

	# Remove all unnecessary characters
	text = text.replace(',', '').replace('.', '').replace('\r\n', '').replace(' ', '')

	# We assume that a tag is beginning with #
	result = text.split('#')

	# Remove all empty entries from the list, see: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
	result = list(filter(None, result))
	return result
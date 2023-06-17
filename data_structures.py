class DictOfValidOutput(dict):
	'''
	- this custom dictionary is made to control the output valúes of the gates
	- valid output of the gates can be one of the value from 'valid_outputs' list
	'''
	def __setitem__(self, key, value):
		valid_outputs = ['0', '1', 0, 1]
		if value in valid_outputs:
			value = int(value)
			super().__setitem__(key, value)
		else:
			raise ValueError(f'''Only '1' and '0' are allowed as output of the gate''')
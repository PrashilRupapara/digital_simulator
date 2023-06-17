from abc import ABC, abstractmethod


class Gate(ABC):
	def __init__(self, name, workspace, output_to) -> None:
		# setting the instance variables
		self.__name = name # updates: case of name duplicates is not handled
		self.input_pins = [] # updates: case of name duplicates is not handled
		self.output_to = output_to
		self.gateName_output_dictionary = workspace.gateName_output_dictionary
		self.gates = workspace.gates

		# default - adding gate to the workspace 
		workspace.add_gate(self)
	
	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self, new_name):
		raise PermissionError("Name can't be changed")
	
	@abstractmethod
	def execute(self):
		pass
	
	def update_input_pins_of_successor_gate(self):
		# adding self.name to the output_to gates as input_pins
		for gate_name in self.output_to:
			self.gates[gate_name].input_pins.append(self.name)

	def update_gateName_output_dictionary(self, ans):
		# setting output for new gate and updating the output for existing gate both case are handled
		self.gateName_output_dictionary[self.name] = ans

	@classmethod
	def available_gates(cls):
		subclasses = set()
		work = [cls]
		# making list of types of childs
		while work:
			parent = work.pop()
			for child in parent.__subclasses__():
				if child not in subclasses:
					subclasses.add(child.__name__)
					work.append(child)

		return subclasses
	
	@staticmethod
	def make_instance_of(string_classname, param_list):
		# Create an instance using the string name
		var = globals()
		var_list = param_list
		instance = var[string_classname](*param_list)
		return instance
		# instance = print(type(globals()[string_classname]))
		# instance = globals()[string_classname](*params)
		# return instance


class OR(Gate):
	def __init__(self, name, workspace, output_to) -> None:
		super().__init__(name, workspace, output_to)
	
	def execute(self):
		ans = 0
		for input_gate in self.input_pins:
			ans = ans or self.gateName_output_dictionary[input_gate]

		self.update_input_pins_of_successor_gate()
		self.update_gateName_output_dictionary(ans)
		return ans


class AND(Gate):
	def __init__(self, name, workspace, output_to) -> None:
		super().__init__(name, workspace, output_to)
	
	def execute(self):
		ans = 1
		for input_gate in self.input_pins:
			ans = ans and self.gateName_output_dictionary[input_gate]

		self.update_input_pins_of_successor_gate()
		self.update_gateName_output_dictionary(ans)
		return ans


class NOT(Gate):
	def __init__(self, name, workspace, output_to) -> None:
		super().__init__(name, workspace, output_to)
	
	def execute(self):
		if len(self.input_pins)==1:
			ans = not self.gateName_output_dictionary[self.input_pins[0]]

			self.update_input_pins_of_successor_gate()
			self.update_gateName_output_dictionary(ans)
			return ans
		else:
			raise ValueError('Execution is not possible for more than one input value')
			# Updates:  addition of input can be limited to 1 so that this error message is not needed


class IN(Gate):
	def __init__(self, name, workspace, output_to) -> None:
		super().__init__(name, workspace, output_to)
		self.input_pins = []  # for input gate input values will be given as input_pins
	
	def execute(self):
		if len(self.input_pins)==1:
			ans = self.input_pins[0]

			self.update_input_pins_of_successor_gate()
			self.update_gateName_output_dictionary(ans)
			return ans
		else:
			raise ValueError('Execution is not possible for more than one input value')
			# Updates:  addition of input can be limited to 1 so that this error message is not needed


class OUT(Gate):
	def __init__(self, name, workspace, output_to) -> None:
		super().__init__(name, workspace, output_to)
		# updates: output list might be empty

	def execute(self, wspace):
		if len(self.input_pins)==1:
			ans = self.gateName_output_dictionary[self.input_pins[0]]

			# adding gate name and output value to the output_gates_with_output_dictionary of the workspace
			wspace.OUT_gates_with_output_dictionary[self.name] = ans
			
			return ans
		else:
			raise ValueError('Execution is not possible for more than one input value')
			# Updates:  addition of input can be limited to 1 so that this error message is not needed


if __name__=='__main__':
	from workspace import Workspace
	workspace1 = Workspace()

	or_gate1 = Gate.make_instance_of('OR', ['G1', workspace1, []])
	or_gate2 = OR('G2', workspace1, ['G1', 'G3'])
	# or_gate2.input_pins.append('G1')
	# or_gate2.input_pins.append('G3')
	
	pass
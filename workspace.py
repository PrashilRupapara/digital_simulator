from data_structures import DictOfValidOutput
from digital_elements import IN, OUT


class Workspace:
	def __init__(self) -> None:
		# setting the instance variables
		self.gates = {}  # dictionary of name and whole object of gate
		self.gateName_output_dictionary = DictOfValidOutput()
		self.next_turn_of = set()  # set of gates which are instance of IN class and while execution list of gates to which the output of the next_turn_of gates will be fed
		self.OUT_gates_with_output_dictionary = {}
	
	def add_gate(self, gate):
		# adding gate to the dictionary of gates
		self.gates[gate.name] = gate

		# if the gate is input gate the add input_gate.output_to gates in the next_turn_of set
		if isinstance(gate, IN):
			self.next_turn_of.update(gate.output_to)
			
			# TODO: add the name of input gates to the output gates if IN
		
		return 0

	def simulate(self):
		continue_ = True
		while continue_:
			# simulation code
			for gate_name in self.next_turn_of.copy():
				# empty the set next_turn_of - because it will be updated by the output gates after every iteration
				self.next_turn_of = set()

				# getting the instance of the gate and executing it
				gate_obj = self.gates[gate_name]
				gate_obj.execute()

				# adding output gates to self.next_turn_of set
				self.next_turn_of.update(gate_obj.output_to)

			
			# if all gates in next_turn_of are OUT gate then terminate 
			for gate_name in self.next_turn_of.copy():
				gate_obj = self.gates[gate_name]
				if isinstance(gate_obj, OUT):
					gate_obj.execute(self) # OUT gate will be executed and output value will be stored in the OUT_gates_with_output_dictionary of workspace
					self.next_turn_of.remove(gate_name)
					

			# termination condition - if length of the self.next_turn_of list is 0 then simulation will not continue
			if len(self.next_turn_of)==0:
				continue_ = False
		return 0
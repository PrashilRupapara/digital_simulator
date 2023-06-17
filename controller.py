from workspace import Workspace
from digital_elements import Gate


class Controller:
    def __init__(self) -> None:
        # setting instance variables
        self.workspace = Workspace() # controller is dealing with its own workspace

    def read_design_file(self, file_path):
        with open(file_path, 'r') as f:
            text = f.read()

            # separating text by line
            text = text.split('\n')
            # making list of available gates
            availabel_gates = Gate.available_gates()

            for line in text:
                # separating text by space
                line = line.split(' ')
                
                # extracting the details from the line
                gate_name = line[0]
                gate_type = line[1]

                # making list of output gates
                del line[0:2] # deleting name and type of the gate
                line = ''.join(line) # making string again
                line = line.replace(', ', ' ') # case 1: '''G1, G2 -> G1 G2'''
                line = line.replace(',', ' ') # case 1: '''G1,G2 -> G1 G2'''
                gate_output_to = line.split(' ')

                # print(gate_name, gate_type, gate_output_to)
                
                # adding gates to the workspace of the controller
                if gate_type in availabel_gates:
                    Gate.make_instance_of(gate_type, [gate_name, self.workspace, gate_output_to])
                else:
                    # handeling the error when wrong gate type is given
                    raise ValueError('Gate of type', gate_type, 'is not available')
        return 0

    def read_stimuli_file(self, file_path):
        with open(file_path, 'r') as f:
            text = f.read()

            # spliting from the space 
            text = text.split(' ')

            # setting input values as available
            ind = 0
            while ind<len(text):
                gate_name = text[ind]
                gate_output = int(text[ind+1])

                # adding read value from the stimuli file to the input_pins of the IN gate(not as name of input gate but as input value)
                in_gate_instance = self.workspace.gates[gate_name]
                in_gate_instance.input_pins.append(gate_output)
                in_gate_instance.execute()
                ind+=2

        return 0

    def simulate(self):
        '''runs the simulate method of the workspace'''
        return self.workspace.simulate()

    def show_output(self):
        ''' prints the gate name and its output from the OUT_gates_with_output_dictionary of the workspace'''
        print('Output: ')
        for key, value in self.workspace.OUT_gates_with_output_dictionary.items():
            print(f'	{key}: {value}')

        return 0


if __name__=='__main__':
    c1 = Controller()
    c1.read_design_file('./design1.txt')
    c1.read_stimuli_file('./stimuli1.txt')
    c1.simulate()
    pass
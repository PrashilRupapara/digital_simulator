from controller import Controller

c1 = Controller()
c1.read_design_file('./design1.txt')
c1.read_stimuli_file('./stimuli1.txt')
c1.simulate()
c1.show_output()
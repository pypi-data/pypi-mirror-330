import matplotlib.pyplot as plt
import warnings
from tabulate import tabulate

from brian2.equations.equations import Equations
from brian2lava_test.utils.files import scrap_folder

class Model():
	"""
	Model(model: dict)
	
	This container class describes a model to be used for the loihi hardware implementation.
	Due to the limited number of Loihi-ready neuron models currently available in Lava, we make a 
	library of available models that the user can pick from. The intended use is to simply feed the
	model equations into the definition of Brian objects. For example,
	`NeuronGroup(10, model = lif.equations())` defines a NeuronGroup with lava-compatible LIF equations.
    The parameter values of this model can then be custimized within Brian/Brian2Lava.

	Brian2Lava also allows the definition of custom models by the user. The requirements for the definition
	of a new model are: 
	- A dictionary containing at least the keys 'ode', 'conditions', and 'parameters'. The most important 
      key is the 'parameters' key.
	  The 'ode' key is mostly for double-checking that the given equations correspond to the expected ones.
      The same holds for the 'conditions' key, which provides information about further conditions such as 
	  threshold crossing or reset. Additionally, the 'ucode_extensions' key may be defined to point to a
      microcode file, and the 'latex' may be used to provide the mathematical description in LaTeX format
	  (for better documentation only).
	- The definition of a Lava Process and ProcessModel(s) to define the actual behavior of the new model
	  (possibly including a file containing the microcode with the behavior of the model to be executed 
      on chip at each timestep).

	Notes:
	------
	Defining a custom model with Loihi support is currently only possible for INRC "Engaged Members" who have
    access to Lava with Loihi extensions (this legal restriction imposed by Intel Labs might be relaxed in
	the future).
	"""

	def __init__(self, model: dict, path = '', name = ''):
		self.model = model
		self.process_name = model['process_name']
		self._equations = Equations('\n'.join(model['ode']))
		self.conditions = model['conditions']
		self.ucode_extensions = model['ucode_extensions']
		self.path = path
		self.name = name
		self.loihi2_ready = False
		for v in self.ucode_extensions.values():
			if not type(v) == str:
				raise TypeError(f"Extensions to look for in the json file must be a dictionary with string values. Instead {v} of type {type(v)} was found.")
			if scrap_folder(self.path,endswith=v,empty_ok=True):
				self.loihi2_ready = True

	@property
	def equations(self):
		"""
		Get ODE equations as Brian `Equations`
		"""
		return self._equations
		
	def show(self):
		"""
		Show equations, variables and parameter from given model
		"""

		# Show latex
		if 'latex' in self.model:
			print("{:<80}".format('Latex equations'))
			print("{:<80}".format('-'*80))
			for idx, l in enumerate(self.model['latex']):
				ax = plt.axes([0,0,0,0]) #left,bottom,width,height
				ax.set_xticks([])
				ax.set_yticks([])
				ax.axis('off')
				plt.text(idx*100, 0, '$%s$' %l, size=25, backgroundcolor='#111111', color='white')
				pl = plt.show()
			print("\n")
			print("{:<80}".format('Raw equations'))
			print("{:<80}".format('-'*80))
			for l in self.model['latex']:
				print("{:<80}".format(l))
			print("\n")
		else:
			warnings.warn('Latex code was not defined in the `model.json`, this is required to be able to show all model details.')

		# List variables
		if 'variables' in self.model:
			print("{:<80}".format('Variables'))
			print("{:<80}".format('-'*80))
			self.print_table('variables')
			print("\n")
		else:
			warnings.warn('Variables were not defined in the `model.json`, please specify to be able to show all model details.')
		
		# List parameters
		if 'parameters' in self.model:
			print("{:<80}".format('Parameters'))
			print("{:<80}".format('-'*80))
			self.print_table('parameters')
		else:
			warnings.warn('Parameters were not defined in the `model.json`, please specify to be able to show all model details.')
	
	def print_table(self,key):
		headers = self.model[key][0].keys()
		table_data = [[item[key] for key in headers] for item in self.model[key]]
		print(tabulate(table_data,headers=headers,tablefmt='grid'))

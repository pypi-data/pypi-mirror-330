import matplotlib.pyplot as plt
from tabulate import tabulate

from brian2.equations.equations import Equations
from brian2lava.utils.files import scrap_folder
from brian2 import get_logger

class Model():
	"""
	This container class serves to describe a neuron model in preset mode. This has become necessary
	for Loihi 2 hardware implementation, however, CPU process models are supported as well. The neuron models are 
	loaded from a defined library. For more details, see the section "Preset model library" in the documentation.
	"""

	def __init__(self, model: dict, path = '', name = ''):
		self.model = model
		self.logger = get_logger('brian2.devices.lava')
		self.process_name = model.get('process_name')
		if not self.process_name:
			self.logger.warn(f'Process name was not defined in `{path}/model.json`, please specify for a correct model description.')
		self.description = model.get('description')
		if 'ode' in self.model:
			self._equations = Equations('\n'.join(model['ode']))
			self._string_equations = '\n'.join(model['ode'])
		else:
			self.logger.warn(f'Brian 2 ODEs were not defined in `{path}/model.json`, please specify for a correct model description.')
			self._equations = None
			self._string_equations = None
		self.conditions = model.get('conditions')
		if not self.conditions:
			self.logger.warn(f'Brian 2 conditions were not defined in `{path}/model.json`, please specify for a correct model description.')
		self.loihi_2_learning_support = model.get('loihi_2_learning_support', False)
		self.ucode_extensions = model.get('ucode_extensions')
		self.variables = set([var['name'] for var in model.get('variables')])
		self.parameters = set([param['name'] for param in model.get('parameters')])
		self.refractory_period = model.get('refractory_period', "")
		self.msb_align_act = set(model.get('msb_align_act', []))
		self.msb_align_decay = set(model.get('msb_align_decay', []))
		self.msb_align_prob = set(model.get('msb_align_prob', []))
		self.path = path
		self.name = name
		self.loihi2_ready = False
		if self.ucode_extensions:
			for v in self.ucode_extensions.values():
				if not type(v) == str:
					raise TypeError(f"Extensions to look for in the json file must be a dictionary with string values. Instead {v} of type {type(v)} was found.")
				if scrap_folder(self.path,endswith=v,empty_ok=True):
					self.loihi2_ready = True
		else:
			self.logger.warn(f'No microcode file extensions were defined in `{path}/model.json`.')
	
	@property
	def string_equations(self):
		"""
		Get model ODEs in a string format which can be used as 
		input to neuron groups. This is useful when string concatenation
		is required, since ``str(Equations(...))`` returns units that are not accepted
		by Brian 2 (e.g., 'V' instead of 'volt').

		Returns
		-------
		`str`
			The equations in string format.
		"""
		return self._string_equations

	@property
	def equations(self):
		"""
		Get ODE equations as Brian-compatible object.
		
		Returns
		-------
		`Equations`
			The equations as Brian `Equations` object.
		"""
		return self._equations
		
	def show(self, latex_rendered = True, latex_raw = False):
		"""
		Show equations, variables, and parameter from given model in LaTeX format.

		Parameters
		---------
		latex_rendered : `bool`, optional
			Specifies whether rendered LaTeX formulas shall be shown as well.
		latex_raw : `bool`, optional
			Specifies whether raw LaTeX formulas shall be shown as well.
		"""
	
		# Function to print table
		def print_table(key):
			if len(self.model[key]) > 0:
				headers = self.model[key][0].keys()
				table_data = [[item[key] for key in headers] for item in self.model[key]]
				print(tabulate(table_data,headers=headers,tablefmt='grid'))

		# Model name
		print("{:<80}".format('Model name (name of the Lava process)'))
		print("{:<80}".format('-'*80))
		print("{:<80}".format(self.name))
		print("\n")

		# Model description
		print("{:<80}".format('Description'))
		print("{:<80}".format('-'*80))
		print("{:<80}".format(self.description))
		print("\n")

		# Show LaTeX
		if 'latex' in self.model:
			if latex_rendered:
				print("{:<80}".format('Model equations (rendered LaTeX)'))
				print("{:<80}".format('-'*80))
				for idx, l in enumerate(self.model['latex']):
					ax = plt.axes([0,0,0,0]) #left,bottom,width,height
					ax.set_xticks([])
					ax.set_yticks([])
					ax.axis('off')
					plt.text(idx*100, 0, '$%s$' %l, size=12, backgroundcolor='#ffffff', color='#111111')
					pl = plt.show()
				print("\n")
			if latex_raw:
				print("{:<80}".format('Model equations (raw LaTeX)'))
				print("{:<80}".format('-'*80))
				for l in self.model['latex']:
					print("{:<80}".format(l))
				print("\n")
		else:
			self.logger.warn('LaTeX code was not defined in the `model.json` file, but this is required to be able to show all model details.')

		# List Brian 2 equations
		print("{:<80}".format('Brian 2 equations'))
		print("{:<80}".format('-'*80))
		for l in self.model['ode']:
			print("{:<80}".format(l))
		print("\n")
		
		# List Brian 2 conditions
		print("{:<80}".format('Brian 2 conditions'))
		print("{:<80}".format('-'*80))
		for key, val in self.model['conditions'].items():
			print("{:<80}".format(str(key) + " : " + str(val)))
		print("\n")

		# List support for refractory period
		print("{:<80}".format('Refractory period'))
		print("{:<80}".format('-'*80))
		if self.refractory_period == "True":
			print("<supported>")
		else:
			print("<not supported>")
		print("\n")
		
		# List Brian 2 variables
		if 'variables' in self.model:
			print("{:<80}".format('Variables'))
			print("{:<80}".format('-'*80))
			print_table('variables')
			print("\n")
		else:
			self.logger.warn('Variables were not defined in the `model.json` file, but this is required to be able to show all model details.')
		
		# List Brian 2 parameters
		if 'parameters' in self.model:
			print("{:<80}".format('Parameters'))
			print("{:<80}".format('-'*80))
			print_table('parameters')
		else:
			self.logger.warn('Parameters were not defined in the `model.json` file, but this is required to be able to show all model details.')

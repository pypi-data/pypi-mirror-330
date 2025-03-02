from types import SimpleNamespace
import os
import json
import warnings
from brian2lava_test.utils.files import scrap_folder
from brian2lava_test.preset_mode.abstract_model import Model
from brian2lava_test.utils.const import HARDWARE
from brian2.utils.logger import get_logger

class ModelLoader:
	# Make a list of available predefined models. We make this a class attribute 
	# so the available models can be printed at any time through 
	# `ModelLoader.available_preset_models()`.
	preset_models = []

	@staticmethod
	def available_preset_models():
		print("Preset models available:\n")
		for model in ModelLoader.preset_models:
			loihi_ready = "Loihi2-ready" if model.loihi2_ready else "CPU-only"
			print(model.name, model.path, loihi_ready, sep=' -- ')
		
		print("\nThese models have been loaded and can be imported from 'brian2lava_test.preset_mode.model_loader' "
		"by their name. Given the currently available models, you might run, for example: "
		f"'from brian2lava_test.preset_mode.model_loader import {ModelLoader.preset_models[0].name}'.")

	@staticmethod
	def read_models(device, user_dir, models_print):
		"""
		Loads models which may then be imported from this static class.

		Parameters
		----------
		device : object
			Object of the Brian device.
		user_dir : str
			A user defined path to read the models from, or ``None`` for models from the Brian2Lava package.
		models_print : bool
		 	Specifies if a list of the models should be printed (can otherwise be done manually by calling 
			`ModelLoader.available_preset_models()`).
		"""
		logger = get_logger(__name__)
		# Init model directories
		model_dirs = {}
		found_models = False

		# Reset list of models (necessary because this is a static class)
		ModelLoader.preset_models = []

		# Package models: models provided by the Brian2Lava team will be stored
		# in the current directory. We load them into the current namespace to allow
		# the user to import them in their scripts.
		# Get current directory, tyring to avoid possible issues in GitLab CI/CD environment
		if os.environ.get('CI') == 'true':
			current_dir = os.path.join(os.getcwd(), 'brian2lava_test', 'preset_mode')
		else:
		    current_dir = os.path.dirname(os.path.abspath(__file__))
		package_dir = os.path.join(current_dir, 'lib', 'model_lib')
		# Get model names and dirs
		model_names_raw = next(os.walk(package_dir))[1]
		pkg_model_names = list(filter(lambda name: not name.startswith('_'), model_names_raw))
		model_dirs = { m: os.path.join(package_dir, m) for m in pkg_model_names }
		logger.debug([model for model in model_dirs])
		# Only go on if there is at least one model defined or the user has specified a model directory.
		if user_dir is not None:
			
			# Get names and dirs
			try:
				usr_model_names = next(os.walk(user_dir))[1]
			except StopIteration:
				raise ValueError(f"The path to the folder containing the preset models is either empty or does not exist: {user_dir}")
			
			for model_name in usr_model_names:
				if model_name in model_dirs:
					logger.warn(
						f"The name of one or more of the models defined in the given model directory {user_dir} "
						"conflicts with the models existing in the base brian2lava library. User-defined models will"
						" always override default ones. If you did not intend for this to happen, rename your model folders.",
						once= True)
					model_dirs.pop(model_name)
			
			model_dirs = { **model_dirs, **{ m: os.path.join(user_dir, m) for m in usr_model_names } }
			# TODO: Make this a bit more general, now it's a bit too strict
			# If no models found, throw an exception
			if not len(usr_model_names):
				warnings.warn(f'Could not find any model. Please add models to the model directory you provided: {user_dir}.')
			
		if not len(model_dirs) and device.mode == 'preset':
			warnings.warn(f"No folders containing preset models were found (not even in '{package_dir}'). Switching device to flexible mode for CPU.")
			device.mode == 'flexible'
			device.hardware == HARDWARE.CPU
			return

		# Iterate over model names, obtained from child folder names
		for name, path in model_dirs.items():

			# Read and parse model files and initialize a `Model`
			model_path = scrap_folder(path,endswith='.json',max_files=1, return_full_path=True, empty_ok= True)
			# If there are irrelevant folders, skip them
			if not len(model_path):
				continue
			model_path = model_path[0]
			with open(model_path, 'rb') as json_file:
				model = Model(json.load(json_file), name = name, path = path)
				ModelLoader.preset_models.append(model)
				
				# Add the model to the globals namespace to make it importable
				# Further provide functions to the added models
				globals()[name] = SimpleNamespace(**{
					'equations': model.equations,
					'conditions': model.conditions,
					'show': model.show
				})
				found_models = True
				logger.debug(f"Found model: '{model.name}' (in '{model_path}').")
		# If we didn't find any model, let the user know
		if not found_models:
			raise ValueError(f"No valid model description file was found in the given folders {model_dirs}.")
		# Print a list of the models
		if models_print:
			ModelLoader.available_preset_models()

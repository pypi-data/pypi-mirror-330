import os
from jinja2 import ChoiceLoader, Environment, StrictUndefined, FileSystemLoader
from brian2.codegen.templates import autoindent, variables_to_array_names, LazyTemplateLoader


class Templater:
	"""
	Class to load and return all the templates a ``CodeObject`` defines.

	This particular implementation replaces ``brian2.codegen.templates.Templater``.
	This is required since Jinja ``PackageLoader`` has a problem with packaging,
	so ``PackageLoader`` is here replaced by ``FileSystemLoader``.

	Parameters
	----------
	package_name : `str`, tuple of `str`
		The package where the templates are saved. If this is a tuple then each template will be searched in order
		starting from the first package in the tuple until the template is found. This allows for derived templates
		to be used. See also the method ``derive()``.
	extension : `str`
		The file extension (e.g. ``.pyx``) used for the templates.
	env_globals : `dict`, optional
		A dictionary of global values accessible by the templates. Can be used for providing utility functions.
		In all cases, the filter 'autoindent' is available (see existing templates for example usage).
	templates_dir : `str`, tuple of `str`, optional
		The name of the directory containing the templates. Defaults to ``'templates'``.

	Notes
	-----
	Templates are accessed using ``templater.template_base_name`` (the base name is without the file extension).
	This returns a ``CodeObjectTemplate``.
	"""

	def __init__(
		self, package_name, extension, env_globals=None, templates_dir="codegen/templates"
	):
		if isinstance(package_name, str):
			package_name = (package_name,)
		if isinstance(templates_dir, str):
			templates_dir = (templates_dir,)

		# Define project root
		project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		
		templateLoader = []
		for t_dir in templates_dir:
			# Get path to templates
			template_path = os.path.join(project_root, t_dir)
			# Define file system loader
			fsl = FileSystemLoader(template_path)
			templateLoader.append(fsl)

		loader = ChoiceLoader(templateLoader)

		self.env = Environment(
			loader=loader,
			trim_blocks=True,
			lstrip_blocks=True,
			undefined=StrictUndefined,
		)
		self.env.globals["autoindent"] = autoindent
		self.env.filters["autoindent"] = autoindent
		self.env.filters["variables_to_array_names"] = variables_to_array_names
		if env_globals is not None:
			self.env.globals.update(env_globals)
		else:
			env_globals = {}
		self.env_globals = env_globals
		self.package_names = package_name
		self.templates_dir = templates_dir
		self.extension = extension
		self.templates = LazyTemplateLoader(self.env, extension)


	def __getattr__(self, item):
		return self.templates.get_template(item)


	def derive(
		self, package_name, extension=None, env_globals=None, templates_dir="templates"
	):
		"""
		Return a new ``Templater`` object derived from this one, where the new package name and globals overwrite the old.

		See the class constructor for the documentation of the parameters.

		Returns
		-------
		`Templater`
			The new ``Templater`` object.
		"""
		
		if extension is None:
			extension = self.extension
		if isinstance(package_name, str):
			package_name = (package_name,)
		if env_globals is None:
			env_globals = {}
		if isinstance(templates_dir, str):
			templates_dir = (templates_dir,)
		package_name = package_name + self.package_names
		templates_dir = templates_dir + self.templates_dir
		new_env_globals = self.env_globals.copy()
		new_env_globals.update(**env_globals)
		return Templater(
			package_name,
			extension=extension,
			env_globals=new_env_globals,
			templates_dir=templates_dir,
		)

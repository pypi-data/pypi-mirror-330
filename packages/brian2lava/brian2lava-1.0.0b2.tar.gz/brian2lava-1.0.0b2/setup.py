from setuptools import setup, Command
import subprocess

class SubmoduleUpdateCommand(Command):
	user_options = []
	def initialize_options(self) -> None:
		pass
	def finalize_options(self) -> None:
		pass
	def run(self) -> None:
		subprocess.call(['echo', 'Updating submodules'])
		# Check which submodules are there
		subprocess.call(['git','submodule'])
		# Update them
		subprocess.call(['git','submodule','init'])
		subprocess.call(['git','submodule','foreach','git pull origin main'])
		subprocess.call(['echo','updated submodules'])

class RunTestsCommand(Command):
	user_options = []
	def initialize_options(self) -> None:
		pass
	def finalize_options(self) -> None:
		pass
	def run(self) -> None:
		from brian2lava.tests.run_tests import RunTests
		RunTests()

setup(
	name='brian2lava',
	version = '1.0.0b2', # TODO fetch this from `brian2lava.__init__.py`
	author='Francesco Negri, Jannik Luboeinski, Carlo Michaelis, Winfried Oed, Tristan Stöber, Andrew Lehr, Christian Tetzlaff', # code contributors first (ranked by number of commits), then other contributing team members
	author_email='mail@jlubo.net',
	cmdclass={
		'submodule_update': SubmoduleUpdateCommand,
		'test': RunTestsCommand
	},
	packages=[
		'brian2lava', 
		'brian2lava.device', 
		'brian2lava.codegen', 
		'brian2lava.utils', 
		'brian2lava.preset_mode',
		'brian2lava.tests',
		'brian2lava.tests.models'
	],
	python_requires='>=3.10',
	url='https://gitlab.com/brian2lava/brian2lava',
	license='MIT',
	description='An open-source Brian 2 interface for the neuromorphic computing framework Lava',
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	package_data = {
		"brian2lava/codegen/templates": ["*.py_"],
		"brian2lava/templates": ["*.py.j2"],
		"brian2lava": ["preset_mode/lib/*"]
	},
    include_package_data=True,
	install_requires=[
		"brian2>=2.7.1",
		"jinja2>=2.7",
		"numpy",
		"pytest",
		"scipy",
		"markupsafe==2.0.1",
		"lava-nc>=0.10.0",
		"matplotlib",
        "tabulate"
	],
	
)

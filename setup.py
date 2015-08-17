from setuptools import setup, find_packages

setup(name='fennec',
      version='0.1.0',
      description='Python project to collect Namespace and Project Information from a Gitlab server and create a report',
      author='Matthew Spah',
      author_email='spahmatther@gmail.com',
      scripts=['fennec/bin/fen_cli.py'],
      packages=find_packages(),
      install_requires=['python-gitlab',
                        'mock',
                        'email'],
      dependency_links=[
          "git+ssh://git@github.com:gpocentek/python-gitlab.git#python-gitlab"
      ],
      zip_safe=False)

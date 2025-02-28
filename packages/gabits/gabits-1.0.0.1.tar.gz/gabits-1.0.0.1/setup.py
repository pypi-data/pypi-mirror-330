from setuptools import setup

setup(name='gabits',
      version='1.0.0.1',
      author='Diogo de J. S. Machado',
      author_email='diogomachado.bioinfo@gmail.com',
      description=('Genetic algorithm implementation based on binary '
                   'representation'),
      long_description_content_type='text/markdown',
      long_description=open('README.md').read(),
      install_requires=['numpy'],
      url='https://github.com/diogomachado-bioinfo/gabits',
      )

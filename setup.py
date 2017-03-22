from setuptools import setup, find_packages

setup(name='pif_importer',
      version='0.0.1',
      url='http://github.com/CitrineInformatics/pif-importer',
      description='Script to import common data formats into Citrination',
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pif-importer = pif_importer:main'
          ]
      },
      install_requires=[
          "pypif",
          "citrination_client",
          "sparks_pif_converters",
          "stevedore"
      ],
      extra_require={
          "dft" : ["dfttopif"],
      }
)

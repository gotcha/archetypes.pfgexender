from setuptools import setup, find_packages
import os

version = '0.1dev'

setup(name='archetypes.pfgextender',
      version=version,
      description="Archetypes content types extended with PloneFormGen",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'test': [
          'Plone',
          'Products.Five',
          'Products.PloneTestCase',
          'collective.testcaselayer'], },
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'Products.PloneFormGen',
          'Products.CMFCore',
          'Products.CMFDynamicViewFTI',
          'Products.GenericSetup',
          'zope.dottedname',
          'zope.interface',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

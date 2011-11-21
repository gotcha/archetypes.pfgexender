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
      extras_require=dict(test=[
          'plone.app.testing',
          'plone.app.bbb_testing',
          ]),
      install_requires=[
          'setuptools',
          'Plone',
          'AccessControl',
          'archetypes.schemaextender',
          'Products.Archetypes',
          'Products.PloneFormGen',
          'Products.CMFCore',
          'Products.CMFDynamicViewFTI',
          'Products.GenericSetup',
          'zope.interface',
          'zope.component',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

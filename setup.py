from distutils.core import setup

setup(
    name='invaana_scout',
    version='1.0.0',
    packages=['invaana_scout',
              'invaana_scout.db',
              'invaana_scout.browsers',
              'invaana_scout.server',
              'tests'
              ],
    url='https://github.com/invaana/invaana_scout',
    license='',
    author='Ravi RT Merugu',
    author_email='rrmerugu@gmail.com',
    description='This is a data aggregation framework for scouting and aggregating Scientific Data. '
)
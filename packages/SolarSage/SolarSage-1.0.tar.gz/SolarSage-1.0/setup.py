from distutils.core import setup
from setuptools import find_packages

setup(name='SolarSage',
      version='1.0',
      packages=find_packages(where='src\\'),  # 查找包的路径
      package_dir={'': 'src'},  # 包的root路径映射到的实际路径
      include_package_data=False,
      package_data={'data': []},
      description="""astrologers for astrologers""",
      long_description="""SolarSage is an open-source backend solution for generating precise astrological charts with modern tooling and
developer-friendly APIs.""",
      author='jiunie9n',
      author_email='xxxxxxx@qq.com',
      url='http://www.xxxxx.com/',  # homepage
      license='MIT',
      install_requires=["astropy", "python-data", "numpy", "packaging", "pandas", "pyerfa", "pyswisseph",
                        "pytz", "PyYAML", "six", "tabulate", "tzdata", "requests", ],
      )

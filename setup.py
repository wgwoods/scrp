try:
    from setuptools import setup #Py2
except ImportError:
    from distutils.core import setup #Py3

setup(
    name="scrp",
    version="0.1",
    packages=["scrp"],
    author="Will Woods",
    author_email="wwoods@redhat.com",
    description="RPM scriptlet parsing/conversion tools",
    license="GPLv3+",
    #keywords="foo bar baz",
    url="https://github.com/wgwoods/scrp.git",

    install_requires=['bashlex>=0.12'],

    entry_points={
        'console_scripts':[
            'scrp=scrp.cmd.main',
        ]
    }
)

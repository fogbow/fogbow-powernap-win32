from setuptools import setup

setup(
    name = "win32powernap",
    version = "0.0.1",
    author = "Abmar Barros",
    author_email = "abmargb@gmail.com",
    description = ("Powernap for Win32."),
    license = "Apache2",
    keywords = "fogbow powernap win32",
    url = "https://github.com/fogbow/fogbow-powernap-win32",
    install_requires=['python-novaclient'],
    packages=['win32powernap']
)

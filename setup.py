from setuptools import setup

setup(
    name="robot-vmlib",
    description="",
    version="0.1",

    author="Miroslav Beka",
    author_email="miroslavbeka@me.com",

    maintainer="Miroslav Beka",
    maintainer_email="miroslavbeka@me.com",

    packages=["VMwareLibrary"],
    package_dir={"VMwareLibrary":"VMwareLibrary"},
    package_data={"VMwareLibrary":["vmware.cfg"]},

    entry_points = {
      "console_scripts" : ["robot-vmlib = VMwareLibrary.__main__:main"]
    }
)

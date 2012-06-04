from setuptools import setup, find_packages

setup(name="Deskwid",
    version = 0.1,
    download_url = "https://github.com/jayrambhia/Deskwid/downloads/tarball/master",
    description = "Twitter stream + imdb + notes",
    author = "Jay Rambhia",
    author_email = "jayrambhia777@gmail.com",
    license = 'BSD',
    packages = find_packages(),
    requires = ["mechanize","oauth2"]
    )

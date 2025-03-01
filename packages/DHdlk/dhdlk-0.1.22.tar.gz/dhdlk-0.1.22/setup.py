from setuptools import setup, find_packages

setup(
    name="DHdlk",
    version="0.1.22",
    packages=find_packages(include=["xntwoger*", "pyarmor_runtime*"]),
    include_package_data=True,  # MANIFEST.in dosyasını kullan
    package_data={
        "": ["*.py", "*.pyd", "*.pyc"],
        "pyarmor_runtime": ["*"],
        "xntwoger/dist/pyarmor_runtime_000000": ["*"],
    },
)

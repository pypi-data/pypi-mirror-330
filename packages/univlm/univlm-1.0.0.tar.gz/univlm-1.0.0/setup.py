from setuptools import setup, find_packages

setup(
    name="univlm",
    version="0.0.4",
    packages=find_packages(where="src",include=["univlm", "univlm.scripts"]),
    package_dir={"": "src"},
    install_requires=[
        "huggingface_hub>=0.20.2",
        "transformers>=4.35.0",
        "diffusers>=0.24.0",
        "fuzzywuzzy>=0.18.0",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "univlm-install=univlm.scripts.install_and_test:run_script",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
)

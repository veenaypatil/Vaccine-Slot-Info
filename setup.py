from setuptools import setup, find_packages

requirements = ['requests', 'click', 'twilio', 'cacheout', 'urllib3']

setup(
    name="slotinfo",
    install_requires=requirements,
    version=1.3,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['slotinfo=slot_info.check_available_slots:main']
    },
)

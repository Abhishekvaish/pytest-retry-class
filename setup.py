from setuptools import setup

setup(
    name="pytest-retry-class",
    author="Abhishek Vaish, Jarosław Tanistra",
    version='0.2.0',
    author_email="vaishabhishek104@gmail.com, jaroslaw.tanistra@gmail.com",
    keywords=["python", "pytest", "retry class", "retry failed test"],
    url='https://github.com/Abhishekvaish/pytest-retry-class',
    license="MIT",
    description="A pytest plugin to rerun entire class on failure",
    long_description=(
        "A pytest plugin that reruns all the tests inside"
        " a class if any test inside the class fails"
    ),
    packages=["pytest_retry_class"],
    install_requires=[
        'pytest>=5.3',
    ],

    # the following makes a plugin available to pytest
    entry_points={
        "pytest11": ["pytest-retry-class = pytest_retry_class.main"]
    },
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)

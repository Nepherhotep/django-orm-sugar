from setuptools import setup, find_packages

__author__ = 'Alexey Zankevich'


setup(
    name="django-orm-sugar",
    version="0.3.2",
    py_modules=['django_orm_sugar'],
    author="Alexey Zankevich",
    author_email="alex.zankevich@gmail.com",
    description="Django ORM sugar library to simplify querying",
    keywords=['Django', 'ORM', 'util', 'sugar'],
    license="MIT",
    platforms=['Platform Independent'],
    url="https://github.com/Nepherhotep/django-orm-sugar",
    install_requires=['django'],
    classifiers=["Framework :: Django :: 1.8",
                 "Development Status :: 5 - Production/Stable",

                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.0",
                 "Programming Language :: Python :: 3.1",
                 "Programming Language :: Python :: 3.2",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5"]
)




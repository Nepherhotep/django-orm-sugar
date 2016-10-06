from setuptools import setup, find_packages

__author__ = 'Alexey Zankevich'


setup(
    name="django-orm-sugar",
    version="0.9.0",
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
                 "Framework :: Django :: 1.9",
                 "Framework :: Django :: 1.10",
                 "Development Status :: 5 - Production/Stable",

                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5"]
)




from setuptools import setup, find_packages

setup(
    name='my-blog-app',  # Уникальное название пакета (проверьте, чтобы оно не было занято в PyPI)
    version='0.1.0',  # Начальная версия
    description='Django blog application for learning and testing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Elberd',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/blog-app',  # URL вашего репозитория (или любой)
    packages=find_packages(),  # Автоматически включает все пакеты (включая app)
    include_package_data=True,  # Включает файлы из MANIFEST.in
    install_requires=[  # Зависимости из requirements.txt
        'asgiref==3.8.1',
        'Django==5.1.6',
        'django-sslserver==0.22',
        'djangorestframework==3.15.2',
        'sqlparse==0.5.3',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
from setuptools import setup, find_packages

setup(
    name='number_fa',  # نام کتابخانه
    version='0.1',
    packages=find_packages(),
    description='A library to convert numbers to Persian words',
    author='Matin jozi',  # نام شما
    author_email='m.matin.jozi@gmail.com',  # ایمیل شما
    url='https://github.com/yourusername/number_fa',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
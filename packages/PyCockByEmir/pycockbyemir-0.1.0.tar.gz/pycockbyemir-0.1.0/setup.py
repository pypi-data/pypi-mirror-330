from setuptools import setup, find_packages

setup(
    name="PyCockByEmir",  # Paket ismi (PyPI'de bu isimle yayımlanacak)
    version="0.1.0",  # Versiyon numarası
    author="Emir",
    author_email="celalinko@gmail.com",
    description="Boy ve ayak uzunluğu hesaplamaları için bir Python kütüphanesi",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EmirKcky/PyCockByEmir",  # GitHub repo linkin
    packages=find_packages(),
    install_requires=[],  # Eğer bağımlılıklar varsa buraya ekleyebilirsin
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

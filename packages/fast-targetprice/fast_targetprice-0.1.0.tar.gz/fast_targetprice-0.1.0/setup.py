from setuptools import setup, find_packages

setup(
    name="fast_targetprice",  # Tên gói trên PyPI (phải là duy nhất)
    version="0.1.0",  # Phiên bản gói
    author="Minh nguyen",
    author_email="minh.worker.117@gmail.com",
    description="Socket price CSGO",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Các thư viện phụ thuộc nếu có
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages

setup(
    name="fast_targetprice",  # Tên gói trên PyPI (phải là duy nhất)
    version="0.1.1",  # Phiên bản gói
    author="Minh nguyen",
    author_email="minh.worker.117@gmail.com",
    description="Socket price CSGO",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Các thư viện phụ thuộc nếu có
    ],
    package_data={
        "fast_targetprice": ["dataset.json"],  # Đảm bảo file JSON được đóng gói
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

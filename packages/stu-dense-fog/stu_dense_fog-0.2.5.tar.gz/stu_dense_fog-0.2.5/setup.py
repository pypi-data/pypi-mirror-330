from setuptools import setup, find_packages

setup(
    name='stu_dense_fog',  # 包名
    version='0.2.5',      # 版本号
    author='Jack-Li',   # 作者名
    author_email='477434296@qq.com',  # 作者邮箱
    description='A dense fog project for STU',  # 描述
    long_description=open('README.md', encoding='utf-8').read(),  # 长描述，通常是README文件的内容
    long_description_content_type='text/markdown',  # 长描述的格式
    url='https://github.com/yourusername/stu_dense_fog',  # 项目的URL
    packages=find_packages(),  # 自动查找包
    classifiers=[  # 分类器，用于告诉用户你的包适用于哪些Python版本等
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 指定支持的Python版本
)

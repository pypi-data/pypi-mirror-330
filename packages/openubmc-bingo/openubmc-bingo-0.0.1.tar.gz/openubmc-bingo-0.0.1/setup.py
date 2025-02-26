from distutils.core import setup
setup(
    name = 'openubmc-bingo',         # 写包的名字
    packages = ['bingo'],   # 写包的名字
    version = '0.0.1',      # Start with a small number and increase it with every change you make
    license='MulanPSL2',        # 选择一个开源许可对应你刚才那个from here: https://help.github.com/articles/licensing-a-repository
    description = 'One',   # Give a short description about your library
    author = 'LiYanghang',                   # 填写作者名称
    author_email = 'author@openubmc.cn',      # 填写email
    url = 'https://www.openubmc.cn',   # Provide either the link to your github or to your website
    download_url = 'https://www.openubmc.cn',    # I explain this later on
    keywords = ['openubmc',  'Python'],   # Keywords that define your package best
    install_requires=[            # 包的依赖
        'requests',       # 可以加上版本号，如validators=1.5.1
        'datetime',
        'urllib3==1.26.6',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # 再次选择
        'Programming Language :: Python :: 3.7',
    ]
)
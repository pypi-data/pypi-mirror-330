
from setuptools import setup, find_packages


setup(name='llm-req',
    version='0.1.5',
    description='llm req client',
    url='https://gitee.com/dark.H/llm-cli.git',
    author='auth',
    author_email='xxx@gmail.com',
    license='MIT',
    include_package_data=True,
    package_data={
        'package_name': ['llm_req/llm_flow/dist/*.html','llm_req/llm_flow/dist/*.ico','llm_req/llm-flow/dist/assets/*.css', 'llm_req/llm-flow/dist/assets/*.js']
    },
    zip_safe=False,
    packages=find_packages(),
    install_requires=['requests','aiohttp','loguru','tqdm'],
    entry_points={
        'console_scripts': [
            'llm-req=llm_req.cmd:main',
            # 'llm-flow=llm_req.llm_flow.main:main'
        ]
    },
    extras_require={
        "server": [
            'pandas',
            'flask',
            'loguru',
            'flask_socketio',
            'flask_sqlalchemy',  
        ],
    },

)

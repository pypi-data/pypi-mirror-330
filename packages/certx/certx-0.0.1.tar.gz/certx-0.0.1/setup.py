import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='certx',
        version='0.0.1',
        description='Generator Self-Signed Private CA and Certificate',
        author='dengshaolin',
        url='https://gitee.com/dengshaolin/certx',
        python_requires='>=3.6',
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={
            'oslo.config.opts': ['certx = certx.conf.opts:list_opts'],
            'console_scripts': ['certx-server = certx.server:start']
        },
        license='Apache 2.0'
    )

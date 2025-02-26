from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="image_dataset_converter_all",
    description="Meta-library that combines all image_dataset_converter libraries.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-datamining/image_dataset_converter-all",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    license='MIT License',
    packages=[],
    install_requires=[
        "image_dataset_converter>=0.0.6",
        "image_dataset_converter_imgaug>=0.0.7",
        "image_dataset_converter_imgstats>=0.0.1",
        "image_dataset_converter_imgvis>=0.0.3",
        "image_dataset_converter_labelme>=0.0.1",
        "image_dataset_converter_paddle>=0.0.1",
        "image_dataset_converter_pdf>=0.0.1",
        "image_dataset_converter_redis>=0.0.2",
        "image_dataset_converter_video>=0.0.1",
    ],
    version="0.0.7",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
)

from setuptools import setup, find_packages

setup(
    name="talklink",
    version="0.0.30",
    author='David Schneck',
    author_email='president@remoria.ai',
    description='Create a talklink page from a youtube video',
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "openai",
        "tiktoken",
        "pydantic",
        "jinja2",
        "assemblyai",
        "requests",
        "librosa",
        "soundfile",
    ],
    python_requires='>=3.10',
    include_package_data=True,
) 
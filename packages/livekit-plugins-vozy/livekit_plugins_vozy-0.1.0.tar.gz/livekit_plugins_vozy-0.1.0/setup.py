from setuptools import setup, find_namespace_packages

setup(
    name="livekit-plugins-vozy",
    version="0.1.0",
    description="LiveKit plugin for Vozy TTS integration",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_namespace_packages(include=["livekit.*"]),
    install_requires=[
        "aiohttp>=3.8.0",
        "livekit>=0.1.0",  # Ajusta según la versión que necesites
    ],
    python_requires=">=3.7",
) 
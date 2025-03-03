from setuptools import setup, find_packages

setup(
    name="genai-assistant",
    version="0.1.0",
    author="Kushagra",
    author_email="radhikayash2@gmail.com",
    description="A Streamlit-powered AI assistant that scrapes your screen.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kushagra2503/genai-assistant",  # Update with your repo
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "google-generativeai",
        "speechrecognition",
        "numpy",
        "pyaudio",
        "opencv-python",
        "pyautogui",
        "gtts",
    ],
    entry_points={
        "console_scripts": [
            "genai-assistant=genai_assistant.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

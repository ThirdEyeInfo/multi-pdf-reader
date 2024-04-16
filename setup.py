from setuptools import find_packages,setup

setup(
    name='Multiple PDF File Reader Chatbot',
    version='0.0.1',
    author='Satyaprakash Nayak',
    author_email='n.satyaprakash@yahoo.com',
    packages=find_packages(),
    install_requires=["streamlit",
                      "pypdf2",
                      "langchain",
                      "python-dotenv",
                      "chroma",
                      "huggingface_hub"]
)
## Step to run Multiple PDF File Reader
- Clone multi-pdf-reader in your local machine
- Download and install Anaconda from https://www.anaconda.com/download
- Type anaconda on windows search and open anaconda command prompt
- Navigate to multi-pdf-reader progect (in step 1) from conda prompt and/by follow below commands
    * cd <basepath>/multi-pdf-reader
    * conda create -n multi-pdf-reader python=3.11 -y
    * conda activate multi-pdf-reader
    * pip install -r requirement.txt
- Create a file with name '.env' in multi-pdf-reader folder
- Add below line in .env file
    * HUGGINGFACEHUB_API_TOKEN="Supply your secret token here"
- Run Multiple PDF File Reader with below command
    * streamlit run app.py --server.port 8080
- Open http://localhost:8080/ on your favorite browser
    * Upload any number of pdf files and ask question related to that
 
### Note: Additional Information
![Screenshot 2024-05-01 164622](https://github.com/ThirdEyeInfo/multi-pdf-reader/assets/93641638/69012354-014a-4e26-b6e8-e7aff75b443f)

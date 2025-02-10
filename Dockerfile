# base image
FROM python:3.11-slim

# Installing python packages
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copying all the code and data
COPY . fin_desk/.

# Expose port for to be access externally
EXPOSE 8501

# Change dir to app folder
WORKDIR /fin_desk/src

# RUN CMD
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]

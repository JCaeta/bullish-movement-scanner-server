# Specify base image
FROM python:3.11.0

# Set the working directory in the container
WORKDIR /server

# Copy all files of our project
COPY . .

# Install dependencies on the image
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "./api.py"]



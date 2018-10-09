# Use an official Python runtime as a parent image
FROM python:3.6-alpine

# Set the working directory 
WORKDIR /home/desnos

# Copy the current directory contents into the container at /home/desnos
COPY . /home/desnos

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World
ENV FOR_DESNOS_ONLY it-May-flower-ev3nt

# Run app.py when the container launches
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]

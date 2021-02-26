# alpine OS with python installed
FROM python:3.7-alpine

# Copy the current directory contents into the container at /app
#ADD . /app
RUN pip install --upgrade pip


WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
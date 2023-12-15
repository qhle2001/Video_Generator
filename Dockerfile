# Use an official Python runtime as a parent image
FROM python:3.9

# Copy the current directory contents into the container at /app
COPY dist/GUI.exe /app/
COPY requirements.txt /app/
COPY *.py /app/
COPY API_KEY.txt /app/
COPY ImageMagick-7.1.1-21.x86_64.rpm /app/
COPY audio /app/
COPY images /app/
COPY results /app/
COPY videos /app/

WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["./GUI.exe"]

FROM python:3.11.2

# Change directory to consumeAPI
WORKDIR /app/consumeAPI

# Copy only the requirements file and install dependencies for consumeAPI
COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the consumeAPI directory
COPY . .

# Command to run on container start
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 consumeMLAPI:app

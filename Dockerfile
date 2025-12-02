# Latest Ubuntu Docker container
FROM ubuntu:latest

# Set a working directory in the container for code and libraries
WORKDIR /code

# Copy all code and configurations into the container
ADD ./lib/*.py ./lib/
ADD ./schemas.py ./schemas.py
ADD ./main.py ./main.py

# Install dependencies (Python pip modules)
RUN apt update; apt full-upgrade -y; apt install python3 python3-fastapi python3-serial python3-hamlib libhamlib-utils uvicorn git -y

# Run main.py on container startup
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app" ]
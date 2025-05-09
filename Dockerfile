# FROM python:3.10-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 5000  
# CMD ["python", "serviceOne.py"]
 
FROM python:3.10-slim
 
WORKDIR /app
 
COPY . .
 
RUN pip install --no-cache-dir flask pika mysql-connector-python
 
CMD ["python", "app.py"]
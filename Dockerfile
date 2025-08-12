# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the whole project
COPY . .

# Expose port 8000
EXPOSE 8080

# Set environment variable for Streamlit to run on port 8000 and allow external connections
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false

# Run the Streamlit app
CMD [CMD ["streamlit", "run", "app.py", "--server.port", "8080" ]

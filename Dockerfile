FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system deps for building wheels if needed
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Non-root user
RUN useradd --create-home appuser
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH

CMD ["python", "-m", "src.main"]

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8503

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8503/_stcore/health', timeout=3)" || exit 1

CMD ["streamlit", "run", "ui/app.py", "--server.port=8503", "--server.address=0.0.0.0", "--server.headless=true"]

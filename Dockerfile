FROM python:3.11-slim

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-luatex \
    texlive-bibtex-extra \
    texlive-lang-all \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# ---- working dir ----
WORKDIR /app

# ---- python deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- app code ----
COPY . .

# ---- runtime ----
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

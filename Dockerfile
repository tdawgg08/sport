FROM python:3.1

COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .
CMD bash -c "python main.py"
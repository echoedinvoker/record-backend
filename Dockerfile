FROM python:3.10 AS build
WORKDIR /app
RUN git clone https://github.com/echoedinvoker/record-backend.git .

FROM python:3.10-slim
WORKDIR /app
COPY --from=build /app /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expone el puerto en el que la aplicación correrá (en este caso, 0)
EXPOSE 5000

# Define el comando de arranque
CMD sh -c 'gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app'

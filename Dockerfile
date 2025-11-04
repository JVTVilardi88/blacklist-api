# Usa una imagen base de Python
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto (incluido .env)
COPY . .

# Asegura que el archivo .env exista
RUN ls -la /app

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto que usa Flask
EXPOSE 5000

# Comando por defecto para ejecutar la app
CMD ["python", "application.py"]

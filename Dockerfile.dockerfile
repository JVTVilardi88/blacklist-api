# Usa una imagen base de Python
FROM python:3.11-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto
COPY . .

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto que usa Flask (ajústalo si tu app usa otro)
EXPOSE 5000

# Comando por defecto para ejecutar la app
CMD ["python", "application.py"]

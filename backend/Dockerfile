# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY ./requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto de desarrollo de Django
EXPOSE 8000

# Comando por defecto (migraciones y servidor en compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

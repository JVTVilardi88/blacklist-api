#!/usr/bin/env python3
"""
Script para probar la conexión a RDS PostgreSQL
"""
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "tu_password_aqui")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blacklist_db")

print("=" * 60)
print("PRUEBA DE CONEXIÓN A RDS PostgreSQL")
print("=" * 60)
print(f"\nHost: {DATABASE_HOST}")
print(f"Puerto: {DATABASE_PORT}")
print(f"Base de datos: {DATABASE_NAME}")
print(f"Usuario: {DATABASE_USER}")
print(f"Password: {'*' * len(DATABASE_PASSWORD)}")
print("\n" + "-" * 60)

try:
    print("\n🔄 Intentando conectar a RDS...")
    
    # Intentar conexión
    connection = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        connect_timeout=10  # Timeout de 10 segundos
    )
    
    # Crear cursor y ejecutar consulta de prueba
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    
    print("✅ CONEXIÓN EXITOSA!")
    print(f"\n📊 Versión de PostgreSQL:")
    print(f"   {db_version[0]}")
    
    # Verificar si existe la tabla blacklist
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'blacklist'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        print("\n✅ Tabla 'blacklist' existe")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM blacklist;")
        count = cursor.fetchone()[0]
        print(f"   Registros en blacklist: {count}")
    else:
        print("\n⚠️  Tabla 'blacklist' NO existe (se creará al iniciar la app)")
    
    # Cerrar conexión
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA - RDS está accesible")
    print("=" * 60)

except psycopg2.OperationalError as e:
    print("\n❌ ERROR DE CONEXIÓN")
    print("\nDetalles del error:")
    print(f"   {str(e)}")
    print("\n🔍 Posibles causas:")
    print("   1. Las credenciales son incorrectas")
    print("   2. El host/puerto es incorrecto")
    print("   3. El Security Group no permite la conexión desde tu IP")
    print("   4. La base de datos no existe")
    print("   5. No hay conectividad de red")
    print("\n💡 Solución:")
    print("   - Verifica las credenciales en el archivo .env")
    print("   - Verifica los Security Groups de RDS en AWS")
    print("   - Asegúrate de estar conectado a la red correcta")
    
except psycopg2.Error as e:
    print("\n❌ ERROR DE BASE DE DATOS")
    print(f"\nDetalles: {str(e)}")
    
except Exception as e:
    print("\n❌ ERROR INESPERADO")
    print(f"\nDetalles: {str(e)}")

print("\n")


import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Popololo928.',
        database='fastapi_demo',
        charset='utf8mb4'
    )
    print("✅ Conexión DIRECTA con pymysql funciona!")
    connection.close()
except Exception as e:
    print(f"❌ Error en conexión directa: {e}")
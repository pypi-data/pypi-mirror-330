# SIGES SDK

SDK para simplificar la comunicación con el core de SIGES para plugins y el manejo de colas de mensajes.

## Instalación

```bash
pip install siges-sdk
```

## Uso básico

### Registro de plugins

```python
import asyncio
from siges_sdk.core import PluginRegisterRequest, Dependencies, Table, get_core_gateway

# Crear tablas de dependencias
tables = [
    Table(name="usuarios", version="1.0.0")
]

# Crear dependencias
dependencies = Dependencies(tables=tables)

# Crear solicitud de registro
request = PluginRegisterRequest(
    name="mi-plugin",
    version="1.0.0",
    port=8080,
    frontend_url="http://localhost:8080/plugin/component/mi-plugin.es.js",
    dependencies=dependencies
)

# Obtener el gateway del core
core_gateway = get_core_gateway()

# Registrar el plugin
async def register_plugin():
    await core_gateway.register_plugin(request)

# Ejecutar la función asíncrona
asyncio.run(register_plugin())
```

### Sistema de colas de mensajes

```python
import asyncio
import json
from siges_sdk.queues import get_message_producer
from siges_sdk.queues.redis_message_consumer import RedisQueueMessageConsumer

# Enviar un mensaje
producer = get_message_producer()
queue_name = "mi-cola"
message = {
    "tipo": "notificacion",
    "contenido": "Este es un mensaje de ejemplo"
}
producer.send_message(queue_name, message)

# Recibir mensajes
async def process_message(message_data):
    print(f"Mensaje recibido: {json.dumps(message_data, indent=2)}")
    return True

# Crear un consumidor
consumer = RedisQueueMessageConsumer(
    queue_name=queue_name,
    callback=process_message,
    consumer_group="mi-grupo",
    max_stream_length=100
)

# Iniciar el consumidor
consumer.start()

# Para detener el consumidor
# consumer.stop()
```

## Características

- Abstracción de la comunicación con el core
- Manejo de dependencias
- Soporte para componentes frontend
- Sistema de colas de mensajes con Redis

## Componentes

### Gateway del Core

El SDK proporciona una interfaz para comunicarse con el core de SIGES:

- `CoreGateway`: Interfaz abstracta para la comunicación con el core
- `get_core_gateway()`: Función para obtener una instancia del gateway

### Modelos de datos

- `PluginRegisterRequest`: Modelo para la solicitud de registro de un plugin
- `Dependencies`: Modelo para las dependencias de un plugin
- `Table`: Modelo para una tabla de dependencia

### Sistema de colas

- `QueueMessageProducer`: Interfaz abstracta para enviar mensajes a una cola
- `QueueMessageConsumer`: Interfaz abstracta para consumir mensajes de una cola
- `get_message_producer()`: Función para obtener una instancia del productor de mensajes
- `RedisQueueMessageConsumer`: Implementación de consumidor de mensajes con Redis

## Desarrollo

### Requisitos

- Python 3.9+
- Docker (para desarrollo y pruebas)

### Configuración del entorno de desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/siges-sdk.git
cd siges-sdk

# Ejecutar el entorno de desarrollo con Docker
docker-compose up sdk
```

### Ejecutar pruebas

```bash
# Usando docker-compose directamente
docker-compose up test

# O usando el comando forge
./forge sdk test

# Para reconstruir las imágenes Docker antes de ejecutar las pruebas
./forge sdk test -b
```

### Ejecutar el ejemplo

```bash
docker-compose up example
```

## Construcción y distribución

### Construir el paquete

Para construir el paquete SDK, puedes usar el comando forge:

```bash
# Construir el paquete SDK
./forge sdk build
```

Esto generará los archivos de distribución en el directorio `dist/`.

### Actualizar la versión

Para actualizar la versión del SDK, puedes usar el comando forge:

```bash
# Actualizar la versión del SDK
./forge sdk upgrade 0.1.1
```

### Instalación del paquete generado

```bash
# Instalar el paquete generado
pip install dist/siges_sdk-*.whl
```

### Publicación como Release de GitHub

La publicación del paquete se realiza a través de un workflow de GitHub Actions. Para publicar una nueva versión:

1. Ve a la pestaña "Actions" en el repositorio de GitHub.
2. Selecciona el workflow "Publish SDK Package" en la lista de workflows.
3. Haz clic en el botón "Run workflow".
4. Ingresa la versión que deseas publicar (en formato X.Y.Z, por ejemplo, 0.1.1).
5. Opcionalmente, marca la casilla "Publicar también en PyPI" si deseas publicar el paquete en PyPI.
6. Haz clic en el botón "Run workflow" para iniciar el proceso de publicación.

El workflow actualizará la versión, construirá el paquete, creará un commit con los cambios de versión, creará una nueva release en GitHub con los archivos del paquete y, si se seleccionó la opción, publicará el paquete en PyPI.

## Licencia

MIT 
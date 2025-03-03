import pytest
from siges_sdk.core import CoreGateway, PluginRegisterRequest, Dependencies, Table, get_core_gateway
from siges_sdk.queues import QueueMessageProducer, get_message_producer, QueueMessageConsumer
from siges_sdk.queues.redis_message_producer import RedisMessageProducer
from siges_sdk.queues.redis_message_consumer import RedisQueueMessageConsumer
import asyncio
from unittest.mock import MagicMock, patch

def test_plugin_register_request_creation():
    """Test que verifica la creación correcta de una solicitud de registro de plugin"""
    # Crear una solicitud básica
    request = PluginRegisterRequest(
        name="test-plugin",
        version="1.0.0",
        port=8080
    )
    
    # Verificar los valores básicos
    assert request.name == "test-plugin"
    assert request.version == "1.0.0"
    assert request.port == 8080
    assert request.frontend_url is None
    assert request.dependencies is None
    
    # Verificar la conversión a diccionario
    request_dict = request.to_dict()
    assert request_dict["name"] == "test-plugin"
    assert request_dict["version"] == "1.0.0"
    assert request_dict["port"] == 8080
    assert "frontend_url" not in request_dict
    assert "dependencies" not in request_dict

def test_plugin_register_request_with_frontend():
    """Test que verifica la creación de una solicitud con URL de frontend"""
    # Crear una solicitud con frontend
    request = PluginRegisterRequest(
        name="test-plugin",
        version="1.0.0",
        port=8080,
        frontend_url="http://localhost:8080/plugin/component/test-plugin.es.js"
    )
    
    # Verificar la URL del frontend
    assert request.frontend_url == "http://localhost:8080/plugin/component/test-plugin.es.js"
    
    # Verificar la conversión a diccionario
    request_dict = request.to_dict()
    assert request_dict["frontend_url"] == "http://localhost:8080/plugin/component/test-plugin.es.js"

def test_plugin_register_request_with_dependencies():
    """Test que verifica la creación de una solicitud con dependencias"""
    # Crear tablas de dependencias
    tables = [
        Table(name="usuarios", version="1.0.0"),
        Table(name="productos", version="2.0.0")
    ]
    
    # Crear dependencias
    dependencies = Dependencies(tables=tables)
    
    # Crear solicitud con dependencias
    request = PluginRegisterRequest(
        name="test-plugin",
        version="1.0.0",
        port=8080,
        dependencies=dependencies
    )
    
    # Verificar las dependencias
    assert request.dependencies is not None
    assert len(request.dependencies.tables) == 2
    assert request.dependencies.tables[0].name == "usuarios"
    assert request.dependencies.tables[0].version == "1.0.0"
    assert request.dependencies.tables[1].name == "productos"
    assert request.dependencies.tables[1].version == "2.0.0"
    
    # Verificar la conversión a diccionario
    request_dict = request.to_dict()
    assert "dependencies" in request_dict
    assert "tables" in request_dict["dependencies"]
    assert len(request_dict["dependencies"]["tables"]) == 2
    assert request_dict["dependencies"]["tables"][0]["name"] == "usuarios"
    assert request_dict["dependencies"]["tables"][1]["name"] == "productos"

def test_gateway_provider():
    """Test que verifica que el proveedor de gateway devuelve una instancia correcta"""
    gateway = get_core_gateway()
    assert isinstance(gateway, CoreGateway)

# Nuevas pruebas para el sistema de colas

def test_message_producer_provider():
    """Test que verifica que el proveedor de productor de mensajes devuelve una instancia correcta"""
    producer = get_message_producer()
    assert isinstance(producer, QueueMessageProducer)
    assert isinstance(producer, RedisMessageProducer)

@patch('redis.Redis')
def test_redis_message_producer_send(mock_redis):
    """Test que verifica el envío de mensajes a través del productor Redis"""
    # Configurar el mock
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    
    # Crear el productor
    producer = RedisMessageProducer()
    
    # Enviar un mensaje
    queue_name = "test-queue"
    message = {"key": "value", "test": 123}
    producer.send_message(queue_name, message)
    
    # Verificar que se llamó a xadd con los parámetros correctos
    mock_redis_instance.xadd.assert_called_once()
    args, kwargs = mock_redis_instance.xadd.call_args
    assert args[0] == queue_name
    # El mensaje debe incluir un ID generado
    assert "id" in kwargs or (len(args) > 1 and "id" in args[1])

@patch('redis.Redis')
def test_redis_message_consumer_init(mock_redis):
    """Test que verifica la inicialización correcta del consumidor Redis"""
    # Configurar el mock
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    
    # Crear una función de callback
    async def callback(message):
        return True
    
    # Crear el consumidor
    queue_name = "test-queue"
    consumer_group = "test-group"
    consumer = RedisQueueMessageConsumer(
        queue_name=queue_name,
        callback=callback,
        consumer_group=consumer_group
    )
    
    # Verificar que se inicializó correctamente
    assert consumer.queue_name == queue_name
    assert consumer.callback == callback
    assert consumer.consumer_group == consumer_group
    assert consumer.is_running == False
    
    # Verificar que se llamó a xgroup_create
    mock_redis_instance.xgroup_create.assert_called_once_with(
        name=queue_name,
        groupname=consumer_group,
        mkstream=True,
        id='0'
    )

@patch('redis.Redis')
def test_redis_message_consumer_start_stop(mock_redis):
    """Test que verifica el inicio y detención del consumidor Redis"""
    # Configurar el mock
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    
    # Crear una función de callback
    async def callback(message):
        return True
    
    # Crear el consumidor
    consumer = RedisQueueMessageConsumer(
        queue_name="test-queue",
        callback=callback,
        consumer_group="test-group"
    )
    
    # Iniciar el consumidor
    consumer.start()
    assert consumer.is_running == True
    
    # Detener el consumidor
    consumer.stop()
    assert consumer.is_running == False 
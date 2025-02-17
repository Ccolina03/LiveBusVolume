from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource,KafkaOffsetsInitializer, KafkaSink, KafkaRecordSerializationSchema, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema, SerializationSchema
from pyflink.datastream.connectors import DeliveryGuarantee
from pyflink.common import Types
import dotenv
from pyflink.common.watermark_strategy import WatermarkStrategy
import json
import lzma
import io
from PIL import Image
import ast
import requests
import numpy as np
import os
from ml_inferencing import generate_volume


def execute(env_file_path):
    environ_vars = dotenv.dotenv_values(env_file_path)
    broker = ""
    input_topic = ""
    output_topic = ""
    api_key = ""
    api_secret = ""
    os_name = os.name
    group_id = "tensorflow_consumer"
    try:
        broker = environ_vars["bootstrap"]
        api_key = environ_vars["api_key"]
        api_secret = environ_vars["api_secret"]
        input_topic = environ_vars["input_topic"]
        output_topic = environ_vars["output_topic"]
    except:
        raise Exception("Env. variables not properly accessed.")
    
    kafa_config = {
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
            "sasl.jaas.config": (
                'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required '
                f'username="{api_key}" '
                f'password="{api_secret}";'
            ),
            "ssl.endpoint.identification.algorithm": "https",
            "connections.max.idle.ms": "30000",
            "reconnect.backoff.ms": "1000",
            "reconnect.backoff.max.ms": "10000"
        }
    
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///C:/Users/abhin/OneDrive/Documents/Computing/2025-Hacked/LiveBusVolume/code/flink/flink-sql-connector-kafka-1.17.2.jar",
                 "file:///C:/Users/abhin/OneDrive/Documents/Computing/2025-Hacked/LiveBusVolume/code/flink/flink-shaded-guava-30.1.1-jre-14.0.jar")
    env.set_parallelism(1)
    source = KafkaSource.builder()\
        .set_bootstrap_servers(broker)\
        .set_topics(input_topic)\
        .set_group_id(group_id)\
        .set_value_only_deserializer(SimpleStringSchema())\
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())\
        .set_properties(kafa_config)\
        .build()
    
    database = KafkaSink.builder()\
        .set_bootstrap_servers(broker)\
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()\
                .set_topic(output_topic)
                .set_value_serialization_schema(SimpleStringSchema())
                .build()
        )\
        .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE)
    
    for key in list(kafa_config.keys()):
        database.set_property(key=key,value=kafa_config[key])
    
    database = database.build()
        
    
    watermark_strategy = WatermarkStrategy.for_monotonous_timestamps()
    ds = env.from_source(source,watermark_strategy=watermark_strategy,source_name="adfsdf")
    
    ds.map(classify,output_type=Types.STRING())
    
    print("Listening for messages")
    env.execute(job_name="demo")

    
def classify(x,env_file="./.env"):
    api = "https://bus-application-ba1a8ce5c80c.herokuapp.com/livebusdata/buses/"
    data : dict = json.loads(x)
    images = []
    for datum in data['frames']:
        bytes = ast.literal_eval(datum)
        decompressed_bytes = lzma.decompress(bytes)
        bytesIO = io.BytesIO(decompressed_bytes)
        image :Image.Image = Image.open(bytesIO).convert("RGB")
        image_array = np.asarray(image)
        images.append(image_array)
    del(data['frames'])
    data['passengers'] = generate_volume(arrays=images)
    del(data['timestamp'])
    print(data)
    
    # Ensure the data correctness
    data['bus_id'] = int(data['bus_id'])
    data['route'] = int(data['route'])
    
    res = requests.post(api,data=data)
    print(res.status_code, "This status code of the request")
    return "Sent"
    
if __name__ == "__main__":
    env_file_path = "./.env"
    execute(env_file_path)
    print("PLs pls pls pls pls")
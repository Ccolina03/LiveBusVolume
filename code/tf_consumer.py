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
import numpy as np
# import tensorflow as tf


def execute(env_file_path):
    environ_vars = dotenv.dotenv_values(env_file_path)
    broker = ""
    input_topic = ""
    output_topic = ""
    api_key = ""
    api_secret = ""
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
    env.add_jars("file:///C:/Users/abhin/OneDrive/Documents/Computing/2025-Hacked/LiveBusVolume/flink-sql-connector-kafka-1.17.2.jar",
                 "file:///C:/Users/abhin/OneDrive/Documents/Computing/2025-Hacked/LiveBusVolume/flink-shaded-guava-30.1.1-jre-14.0.jar")
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

    ds.map(classify,output_type=Types.STRING()).sink_to(database)
    env.execute(job_name="demo")
# def return_volume(image:np.ndarray)->int:
#     model_location = './efficientdet_d0_coco17_tpu-32'
#     model = tf.saved_model.load(model_location)
#     tensor = tf.convert_to_tensor(image)
#     tensor = tensor[tf.newaxis,...]
#     detections : dict = model(tensor)
    
#     num_detections = len(detections['detection_boxes'][0])
#     volume = 0
    
#     for i in range(num_detections):
#         detected = 0
#         if detections['detection_classes'][0][i] == 1 and detections['detection_scores'][0][i] > 0.5:
#             detected = 1
#         volume += detected
    
#     return volume
    
def classify(x):
    data : dict = json.loads(x)
    data['og_bytes'] = ast.literal_eval(data['frame'])
    del(data['frame'])
    image = lzma.decompress(data['og_bytes'])
    del(data['og_bytes'])
    image = io.BytesIO(image)
    image :Image.Image = Image.open(image).convert("RGB")
    array = np.asarray(image)
    # volume = return_volume(array)
    data['volume'] = array.shape[0]
    
    print(f"Sending data for {data['bus_id']}")
    return json.dumps(data)
    
if __name__ == "__main__":
    env_file_path = "./.env"
    execute(env_file_path)
    print("PLs pls pls pls pls")
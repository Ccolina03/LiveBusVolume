package io.confluent.developer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Properties;
import java.util.Random;
import java.util.UUID;

import static org.apache.kafka.clients.CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG;
import static org.apache.kafka.clients.CommonClientConfigs.SECURITY_PROTOCOL_CONFIG;
import static org.apache.kafka.clients.producer.ProducerConfig.*;
import static org.apache.kafka.common.config.SaslConfigs.*;

public class ProducerExample {

    public static void main(final String[] args) {
        final Properties props = new Properties() {{
            // Load sensitive values from environment variables
            put(BOOTSTRAP_SERVERS_CONFIG, System.getenv("KAFKA_BOOTSTRAP_SERVERS"));
            put(SASL_JAAS_CONFIG, "org.apache.kafka.common.security.plain.PlainLoginModule required username='"
                    + System.getenv("KAFKA_USERNAME") + "' password='" + System.getenv("KAFKA_PASSWORD") + "';");

            // Fixed properties
            put(KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getCanonicalName());
            put(VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getCanonicalName());
            put(ACKS_CONFIG, "all");
            put(SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
            put(SASL_MECHANISM, "PLAIN");
        }};

        final String topic = "database";
        final Random rnd = new Random();
        //Serialize JSON test
        final ObjectMapper objectMapper = new ObjectMapper(); 

        try (final Producer<String, String> producer = new KafkaProducer<>(props)) {
            final int numMessages = 2;

            for (int i = 0; i < numMessages; i++) {
                // Create JSON event
                ProcessedImageData event = new ProcessedImageData(System.currentTimeMillis(), rnd.nextInt(1000), rnd.nextInt(100));
                String jsonEvent = objectMapper.writeValueAsString(event);

                producer.send(
                        new ProducerRecord<>(topic, String.valueOf(event.id), jsonEvent),
                        (metadata, ex) -> {
                            if (ex != null)
                                ex.printStackTrace();
                            else
                                System.out.printf("Produced event to topic %s: key = %-10s value = %s%n", topic, event.id, jsonEvent);
                        });
            }

            System.out.printf("%s events were produced to topic %s%n", numMessages, topic);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

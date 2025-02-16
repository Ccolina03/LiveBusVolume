package io.confluent.developer;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.bson.Document;
import com.src.main.java.model.ProcessedImageData;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

import static org.apache.kafka.clients.CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG;
import static org.apache.kafka.clients.CommonClientConfigs.SECURITY_PROTOCOL_CONFIG;
import static org.apache.kafka.clients.consumer.ConsumerConfig.*;
import static org.apache.kafka.common.config.SaslConfigs.*;

/**
 * Kafka Consumer that reads JSON messages from Kafka and inserts them into MongoDB
 */
public class MongoDBConsumer {

    public static void main(final String[] args) {

        // Kafka Consumer Properties
        final Properties props = new Properties();
        props.put(BOOTSTRAP_SERVERS_CONFIG, System.getenv("KAFKA_BOOTSTRAP_SERVERS"));
        props.put(SASL_JAAS_CONFIG, "org.apache.kafka.common.security.plain.PlainLoginModule required username='"
                + System.getenv("KAFKA_USERNAME") + "' password='" + System.getenv("KAFKA_PASSWORD") + "';");
        props.put(KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getCanonicalName());
        props.put(VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getCanonicalName());
        props.put(GROUP_ID_CONFIG, "mongo-consumer-group");
        props.put(AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SASL_MECHANISM, "PLAIN");

        final String topic = "database";

        // Connect to MongoDB
        MongoClient mongoClient = new MongoClient("localhost", 27017);
        MongoDatabase database = mongoClient.getDatabase("kafkaDB");
        MongoCollection<Document> collection = database.getCollection("events");

        // Create Kafka Consumer
        try (final Consumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(topic));

            // JSON Object Mapper
            ObjectMapper objectMapper = new ObjectMapper();

            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Consumed event from topic %s: key = %-10s value = %s%n", topic, record.key(), record.value());

                    try {
                        // Convert JSON string to Java Object
                        ProcessedImageData event = objectMapper.readValue(record.value(), ProcessedImageData.class);

                        // Convert Java Object to MongoDB Document
                        Document doc = new Document("timestamp", event.timestamp)
                                .append("id", event.id)
                                .append("count", event.count);

                        // Insert into MongoDB
                        collection.insertOne(doc);
                        System.out.println("Inserted into MongoDB: " + doc.toJson());
                    } catch (Exception e) {
                        System.err.println("Error parsing JSON: " + e.getMessage());
                        e.printStackTrace();
                    }
                }
            }
        } finally {
            mongoClient.close();
        }
    }
}

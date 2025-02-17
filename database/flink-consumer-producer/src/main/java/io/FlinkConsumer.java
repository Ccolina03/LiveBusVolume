package io;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;
import org.apache.flink.api.connector.source.util.ratelimit.RateLimiter;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.streaming.api.functions.source.datagen.DataGeneratorSource;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;

// Kafka client imports
import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.common.config.SaslConfigs;

public class FlinkConsumer {
    public static void main(String[] args) throws Exception {

        // Load properties from the client.properties file located in the Windows file system
        Properties properties = new Properties();
        
        // File path for the client.properties file (make sure this is accessible from WSL)
        String clientPropertiesPath = "/mnt/c/Users/Carlos/hacked-2025/LiveBusVolume/database/flink-consumer-producer/src/main/resources/client.properties";
        
        try (FileInputStream input = new FileInputStream(clientPropertiesPath)) {
            properties.load(input);
        } catch (IOException e) {
            throw new IllegalStateException("Unable to load properties from client.properties", e);
        }

        // Retrieve Kafka configurations from the loaded properties
        String kafkaBootstrapServers = properties.getProperty("kafka.bootstrap.servers");
        String kafkaUsername = properties.getProperty("kafka.username");
        String kafkaPassword = properties.getProperty("kafka.password");

        // Check if required properties are available
        if (kafkaBootstrapServers == null || kafkaUsername == null || kafkaPassword == null) {
            throw new IllegalStateException("Missing Kafka configuration in client.properties.");
        }

        // Create the execution environment
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Build the KafkaSource with all necessary properties for Confluent Cloud
        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                // Set the bootstrap server from the properties file
                .setBootstrapServers(kafkaBootstrapServers)
                // Set the topic name (here "database")
                .setTopics("database")
                // Set a group id for the consumer
                .setGroupId("flink-database-consumer")
                // Start reading from the earliest offset
                .setStartingOffsets(OffsetsInitializer.earliest())
                // Specify that the deserializer should produce Strings
                .setValueOnlyDeserializer(new SimpleStringSchema())
                // Set the required security properties for Kafka
                .setProperty(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL")
                .setProperty(SaslConfigs.SASL_MECHANISM, "PLAIN")
                .setProperty(SaslConfigs.SASL_JAAS_CONFIG,
                        "org.apache.kafka.common.security.plain.PlainLoginModule required username='"
                        + kafkaUsername
                        + "' password='"
                        + kafkaPassword + "';")
                .build();

        // Create a DataStream from the Kafka source
        DataStream<String> stream = env.fromSource(
                kafkaSource, 
                WatermarkStrategy.noWatermarks(), 
                "Kafka Source");

        // Print out the records from Kafka
        stream.print();

        // Execute the Flink job
        env.execute("Flink Kafka Integration");
    }
}

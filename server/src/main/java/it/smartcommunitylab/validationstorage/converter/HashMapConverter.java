package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.io.Serializable;
import java.util.Map;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class HashMapConverter implements AttributeConverter<Map<String, Serializable>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(Map<String, Serializable> map) {

        String json = null;
        if (map != null) {
            try {
                json = objectMapper.writeValueAsString(map);
            } catch (final JsonProcessingException e) {
            }
        }
        return json;
    }

    @SuppressWarnings("unchecked")
    @Override
    public Map<String, Serializable> convertToEntityAttribute(String json) {

        Map<String, Serializable> map = null;
        if (json != null) {
            try {
                map = objectMapper.readValue(json, Map.class);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
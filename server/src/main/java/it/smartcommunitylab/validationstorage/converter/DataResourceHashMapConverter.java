package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.MapType;

import it.smartcommunitylab.validationstorage.model.DataResource;

public class DataResourceHashMapConverter implements AttributeConverter<Map<String, DataResource>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(Map<String, DataResource> map) {
        String json = null;
        
        if (map != null) {
            try {
                json = objectMapper.writeValueAsString(map);
            } catch (final JsonProcessingException e) {
            }
        }
        
        return json;
    }

    @Override
    public Map<String, DataResource> convertToEntityAttribute(String json) {

        Map<String, DataResource> map = null;
        if (json != null) {
            try {
                MapType mapType = objectMapper.getTypeFactory().constructMapType(HashMap.class, String.class, DataResource.class);
                map = objectMapper.readValue(json, mapType);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
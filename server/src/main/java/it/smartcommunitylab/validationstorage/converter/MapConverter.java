package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.MapType;

public abstract class MapConverter<T extends Serializable> implements AttributeConverter<Map<String, T>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final MapType typeRef;
    
    protected MapConverter(Class<?> targetClass) {
        typeRef = objectMapper.getTypeFactory().constructMapType(HashMap.class, String.class, targetClass);
    }
    

    @Override
    public String convertToDatabaseColumn(Map<String, T> map) {
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
    public Map<String, T> convertToEntityAttribute(String json) {

        Map<String, T> map = null;
        if (json != null) {
            try {
                map = objectMapper.readValue(json, typeRef);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
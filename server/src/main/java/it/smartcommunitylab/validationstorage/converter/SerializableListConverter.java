package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.persistence.AttributeConverter;

import org.springframework.util.StringUtils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

public class SerializableListConverter implements AttributeConverter<List<Serializable>, String> {
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    @Override
    public String convertToDatabaseColumn(List<Serializable> list) {
        
        String json = null;
        if (list != null) {
            try {
                json = objectMapper.writeValueAsString(list);
            } catch (final JsonProcessingException e) {
            }
        }
        return json;
    }

    @SuppressWarnings("unchecked")
    @Override
    public List<Serializable> convertToEntityAttribute(String json) {
        
        List<Serializable> list = null;
        if (json != null) {
            try {
                list = objectMapper.readValue(json, List.class);
            } catch (final IOException e) {
            }

        }
        return list;
    }

}
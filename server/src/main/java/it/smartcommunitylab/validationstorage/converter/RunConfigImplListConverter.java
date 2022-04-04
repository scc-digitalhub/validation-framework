package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.persistence.AttributeConverter;

import org.springframework.util.StringUtils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;

import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

public class RunConfigImplListConverter implements AttributeConverter<List<RunConfigImpl>, String> {
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    @Override
    public String convertToDatabaseColumn(List<RunConfigImpl> list) {
        
        String json = null;
        if (list != null) {
            try {
                json = objectMapper.writeValueAsString(list);
            } catch (final JsonProcessingException e) {
            }
        }
        return json;
    }

    @Override
    public List<RunConfigImpl> convertToEntityAttribute(String json) {
        List<RunConfigImpl> list = null;
        
        if (json != null) {
            try {
                CollectionType listType = objectMapper.getTypeFactory().constructCollectionType(ArrayList.class, RunConfigImpl.class);
                list = objectMapper.readValue(json, listType);
            } catch (final IOException e) {
            }
        }
        
        return list;
    }

}
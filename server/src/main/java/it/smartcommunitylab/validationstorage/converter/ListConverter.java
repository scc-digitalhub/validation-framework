package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;

public abstract class ListConverter<T extends Serializable> implements AttributeConverter<List<T>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final CollectionType typeRef;
    
    protected ListConverter(Class<?> targetClass) {
        typeRef = objectMapper.getTypeFactory().constructCollectionType(ArrayList.class, targetClass);
    }
    

    @Override
    public String convertToDatabaseColumn(List<T> list) {
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
    public List<T> convertToEntityAttribute(String json) {

        List<T> list = null;
        if (json != null) {
            try {
                list = objectMapper.readValue(json, typeRef);
            } catch (final IOException e) {
            }

        }
        return list;
    }

}
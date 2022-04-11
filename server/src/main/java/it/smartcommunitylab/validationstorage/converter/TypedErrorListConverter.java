package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;

import it.smartcommunitylab.validationstorage.typed.TypedError;

public class TypedErrorListConverter implements AttributeConverter<List<TypedError>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(List<TypedError> map) {

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
    public List<TypedError> convertToEntityAttribute(String json) {
        List<TypedError> list = null;
        
        if (json != null) {
            try {
                CollectionType listType = objectMapper.getTypeFactory().constructCollectionType(ArrayList.class, TypedError.class);
                list = objectMapper.readValue(json, listType);
            } catch (final IOException e) {
            }
        }
        
        return list;
    }

}
package it.smartcommunitylab.validationstorage.repository;

import java.io.IOException;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.model.TypedError;

public class TypedErrorConverter implements AttributeConverter<TypedError, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(TypedError map) {

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
    public TypedError convertToEntityAttribute(String json) {

        TypedError map = null;
        if (json != null) {
            try {
                map = objectMapper.readValue(json, TypedError.class);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.typed.TypedConstraint;

public class TypedConstraintConverter implements AttributeConverter<TypedConstraint, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(TypedConstraint map) {

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
    public TypedConstraint convertToEntityAttribute(String json) {

        TypedConstraint map = null;
        if (json != null) {
            try {
                map = objectMapper.readValue(json, TypedConstraint.class);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
package it.smartcommunitylab.validationstorage.converter;

import java.io.IOException;

import javax.persistence.AttributeConverter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.typed.TypedSchema;

public class TypedSchemaConverter implements AttributeConverter<TypedSchema, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(TypedSchema map) {

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
    public TypedSchema convertToEntityAttribute(String json) {

        TypedSchema map = null;
        if (json != null) {
            try {
                map = objectMapper.readValue(json, TypedSchema.class);
            } catch (final IOException e) {
            }

        }
        return map;
    }

}
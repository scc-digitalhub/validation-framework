package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class TypedConstraint {
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    private String type;
    
    @JsonCreator
    public static TypedConstraint create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("frictionless".equals(type)) {
            return objectMapper.convertValue(map, FrictionlessConstraint.class);
        } else if ("duckdb".equals(type)) {
            return objectMapper.convertValue(map, DuckDBConstraint.class);
        }
        
        throw new IllegalArgumentException("Invalid constraint type.");
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}

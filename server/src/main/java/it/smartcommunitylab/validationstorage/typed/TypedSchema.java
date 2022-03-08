package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class TypedSchema {
private static final ObjectMapper objectMapper = new ObjectMapper();
    
    private String type;
    
    @JsonCreator
    public static TableSchema create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("table".equals(type)) {
            return objectMapper.convertValue(map, TableSchema.class);
        }
        
        throw new IllegalArgumentException("Invalid schema type.");
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}

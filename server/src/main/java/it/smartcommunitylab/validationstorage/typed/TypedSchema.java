package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class TypedSchema implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 6197645553735804919L;

    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    protected String type;
    
    static {
        objectMapper.setSerializationInclusion(Include.NON_NULL);
    }
    
    @JsonCreator
    public static TableSchema create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("table".equalsIgnoreCase(type)) {
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

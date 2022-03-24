package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.typed.TableSchema.ColumnField;

public abstract class TypedSchema implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 6197645553735804919L;

    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    private String type;
    
    @JsonCreator
    public static TableSchema create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("table".equals(type)) {
            // TODO convertValue not working for some reason
            TableSchema ts = new TableSchema();
            ts.setType(type);
            ts.setFields((List<ColumnField>) map.get("fields"));
            //TableSchema ts = objectMapper.convertValue(map, TableSchema.class);
            return ts;
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

package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class TypedError {
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    private String constraintId;
    
    private String type;
    
    private String code;
    
    private String note;
    
    @JsonCreator
    public static TypedError create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("frictionless".equals(type)) {
            return objectMapper.convertValue(map, FrictionlessError.class);
        } else if ("duckdb".equals(type)) {
            return objectMapper.convertValue(map, DuckDBError.class);
        }
        
        throw new IllegalArgumentException("Invalid error type.");
    }
    
    public String getConstraintId() {
        return constraintId;
    }

    public void setConstraintId(String constraintId) {
        this.constraintId = constraintId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getNote() {
        return note;
    }

    public void setNote(String note) {
        this.note = note;
    }
    
}

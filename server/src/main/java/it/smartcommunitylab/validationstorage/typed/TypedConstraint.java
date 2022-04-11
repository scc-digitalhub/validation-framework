package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.typed.DuckDBConstraint.Check;

public abstract class TypedConstraint implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 4330448684174457132L;

    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    protected String type;
    
    static {
        objectMapper.setSerializationInclusion(Include.NON_NULL);
    }
    
    @JsonCreator
    public static TypedConstraint create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("frictionless".equalsIgnoreCase(type)) {
            return objectMapper.convertValue(map, FrictionlessConstraint.class);
        } else if ("duckdb".equalsIgnoreCase(type)) {
            DuckDBConstraint mappedConstraint = objectMapper.convertValue(map, DuckDBConstraint.class);
            if (mappedConstraint.getCheck() == null)
                mappedConstraint.setCheck(Check.ROWS);
            
            return mappedConstraint;
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

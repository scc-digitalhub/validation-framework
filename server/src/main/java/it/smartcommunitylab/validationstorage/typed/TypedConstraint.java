package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.ObjectMapper;

import it.smartcommunitylab.validationstorage.typed.DuckDBConstraint.Expect;
import it.smartcommunitylab.validationstorage.typed.FrictionlessConstraint.ConstraintType;

public abstract class TypedConstraint implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 4330448684174457132L;

    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    protected String type;
    
    @JsonCreator
    public static TypedConstraint create(Map<String, Serializable> map) {
        String type = map.get("type").toString();
        
        if ("frictionless".equals(type)) {
            FrictionlessConstraint constraint = new FrictionlessConstraint();
            constraint.type = type;
            constraint.setField(map.get("field").toString());
            constraint.setFieldType(FieldType.fromString(map.get("fieldType").toString()));
            constraint.setConstraintType(ConstraintType.fromString(map.get("constraintType").toString()));
            constraint.setValue(map.get("value").toString());
            return constraint;
            //return objectMapper.convertValue(map, FrictionlessConstraint.class);
        } else if ("duckdb".equals(type)) {
            DuckDBConstraint constraint = new DuckDBConstraint();
            constraint.setQuery(map.get("query").toString());
            constraint.setExpect(Expect.fromString(map.get("expect").toString()));
            constraint.setValue(map.get("value").toString());
            return constraint;
            //return objectMapper.convertValue(map, DuckDBConstraint.class);
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

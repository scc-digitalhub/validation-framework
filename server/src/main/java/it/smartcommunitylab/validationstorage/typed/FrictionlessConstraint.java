package it.smartcommunitylab.validationstorage.typed;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonValue;

@Valid
public class FrictionlessConstraint extends TypedConstraint {
    /**
     * 
     */
    private static final long serialVersionUID = 4274019544371560158L;

    private String field;
    
    private FieldType fieldType;
    
    @JsonProperty("constraint")
    private ConstraintType constraintType;
    
    @NotNull
    private String value;
    
    enum ConstraintType {
        REQUIRED("required"),
        UNIQUE("unique"),
        MIN_LENGTH("minLength"),
        MAX_LENGTH("maxLength"),
        MINIMUM("minimum"),
        MAXIMUM("maximum"),
        PATTERN("pattern"),
        ENUM_TYPE("enumType"),
        TYPE("type"),
        FORMAT("format");
        
        public final String label;
        
        private ConstraintType(String label) {
            this.label = label;
        }
        
        @JsonValue
        public String getLabel() {
            return label;
        }
        
    }

    public String getField() {
        return field;
    }

    public void setField(String field) {
        this.field = field;
    }

    public FieldType getFieldType() {
        return fieldType;
    }

    public void setFieldType(FieldType fieldType) {
        this.fieldType = fieldType;
    }

    public ConstraintType getConstraintType() {
        return constraintType;
    }

    public void setConstraintType(ConstraintType constraintType) {
        this.constraintType = constraintType;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public static long getSerialversionuid() {
        return serialVersionUID;
    }
    
}

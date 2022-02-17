package it.smartcommunitylab.validationstorage.model;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

@Valid
public class FrictionlessConstraint extends TypedConstraint {
    private String field;
    
    private FieldType fieldType;
    
    private FrictionlessType frictionlessType;
    
    @NotNull
    private String value;
    
    enum FieldType {
        string,
        number,
        integer,
        booleanType,
        object,
        array,
        date,
        time,
        datetime,
        year,
        yearmonth,
        duration,
        geopoint,
        geojson,
        any
    }
    
    enum FrictionlessType {
        required,
        unique,
        minLength,
        maxLength,
        minimum,
        maximum,
        pattern,
        enumType
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

    public FrictionlessType getFrictionlessType() {
        return frictionlessType;
    }

    public void setFrictionlessType(FrictionlessType frictionlessType) {
        this.frictionlessType = frictionlessType;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}

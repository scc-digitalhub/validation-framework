package it.smartcommunitylab.validationstorage.typed;

import com.fasterxml.jackson.annotation.JsonValue;

public enum FieldType {
    STRING("string"),
    NUMBER("number"),
    INTEGER("integer"),
    BOOLEAN_TYPE("booleanType"),
    OBJECT("object"),
    ARRAY("array"),
    DATE("date"),
    TIME("time"),
    DATETIME("datetime"),
    YEAR("year"),
    YEARMONTH("yearmonth"),
    DURATION("duration"),
    GEOPOINT("geopoint"),
    GEOJSON("geojson"),
    ANY("any");
    
    public final String label;
    
    private FieldType(String label) {
        this.label = label;
    }
    
    @JsonValue
    public String getLabel() {
        return label;
    }
    
    public static FieldType fromString(String s) {
        for (FieldType e : FieldType.values()) {
            if (e.label.equalsIgnoreCase(s)) {
                return e;
            }
        }
        
        throw new IllegalArgumentException("FieldType: '" + s + "' is not supported.");
    }
}

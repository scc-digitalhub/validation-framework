package it.smartcommunitylab.validationstorage.typed;

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
}

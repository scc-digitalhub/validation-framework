package it.smartcommunitylab.validationstorage.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum ResourceType {
    TABLE("table");
    
    public final String label;
    
    private ResourceType(String label) {
        this.label = label;
    }
    
    @JsonValue
    public String getLabel() {
        return label;
    }
}
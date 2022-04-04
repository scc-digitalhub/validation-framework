package it.smartcommunitylab.validationstorage.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum RunStatus {
    PENDING("pending"),
    RUNNING("running"),
    SUCCESS("success"),
    ERROR("error");
    
    public final String label;
    
    private RunStatus(String label) {
        this.label = label;
    }
    
    @JsonValue
    public String getLabel() {
        return label;
    }
}
package it.smartcommunitylab.validationstorage.model;

public enum RunStatus {
    PENDING("pending"),
    RUNNING("running"),
    SUCCESS("success"),
    ERROR("error");
    
    public final String label;
    
    private RunStatus(String label) {
        this.label = label;
    }
}
package it.smartcommunitylab.validationstorage.model;

public class DuckDBError extends TypedError {
    
    private String description;

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

}

package it.smartcommunitylab.validationstorage.typed;

public class DuckDBError extends TypedError {
    /**
     * 
     */
    private static final long serialVersionUID = 8080154613514625017L;
    
    private String description;

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

}

package it.smartcommunitylab.validationstorage.model.dto;

public class SchemaDTO {
    private String id;
    
    private DataResourceDTO resource;
    
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public DataResourceDTO getResource() {
        return resource;
    }

    public void setResource(DataResourceDTO resource) {
        this.resource = resource;
    }
    
}

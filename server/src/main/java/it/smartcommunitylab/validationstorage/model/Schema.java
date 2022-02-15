package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Schema {
    @Id
    @GeneratedValue
    private long id;
    
    private Resource resource;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public Resource getResource() {
        return resource;
    }

    public void setResource(Resource resource) {
        this.resource = resource;
    }
}

package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Schema {
    @Id
    @GeneratedValue
    private long id;

    private long resourceId;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

}

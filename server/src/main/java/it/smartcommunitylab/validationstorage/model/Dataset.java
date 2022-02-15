package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Embeddable;

@Embeddable
public class Dataset {

    private String path;

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

}
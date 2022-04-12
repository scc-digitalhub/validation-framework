package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;

import javax.persistence.Embeddable;

@Embeddable
public class Dataset implements Serializable {

    /**
     * 
     */
    private static final long serialVersionUID = 1842667154351552110L;
    
    private String path;

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

}
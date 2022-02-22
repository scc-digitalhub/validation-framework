package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Embeddable;

@Embeddable
public class RunConfigImpl {
    private Boolean enable;
    
    private String type;
    
    private String library;

    public Boolean getEnable() {
        return enable;
    }
    
    public boolean isEnabled() {
        return enable != null ? enable.booleanValue() : false;
    }

    public void setEnable(Boolean enable) {
        this.enable = enable;
    }
    
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getLibrary() {
        return library;
    }

    public void setLibrary(String library) {
        this.library = library;
    }
    
}

package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Embeddable;

@Embeddable
public class RunConfigImpl {
    private boolean enable = false;

    public boolean getEnable() {
        return enable;
    }

    public void setEnable(boolean enable) {
        this.enable = enable;
    }
}

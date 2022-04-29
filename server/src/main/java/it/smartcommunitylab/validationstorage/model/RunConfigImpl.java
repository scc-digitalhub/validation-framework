package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.Map;

import javax.persistence.Convert;
import javax.persistence.Embeddable;
import javax.persistence.Lob;

import it.smartcommunitylab.validationstorage.converter.SerializableMapConverter;

@Embeddable
public class RunConfigImpl implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = -1493624082013576419L;

    private Boolean enable;
    
    private String type;
    
    private String library;
    
    @Lob
    @Convert(converter = SerializableMapConverter.class)
    private Map<String, Serializable> execArgs;
    
    @Override
    public String toString() {
        return "RunConfigImpl - enable:" + enable + ", type:" + type + ", library:" + library;
    }
    
    public boolean isEnable() {
        return enable != null ? enable.booleanValue() : false;
    }

    public Boolean getEnable() {
        return enable;
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
    
    public Map<String, Serializable> getExecArgs() {
        return execArgs;
    }

    public void setExecArgs(Map<String, Serializable> execArgs) {
        this.execArgs = execArgs;
    }
    
}

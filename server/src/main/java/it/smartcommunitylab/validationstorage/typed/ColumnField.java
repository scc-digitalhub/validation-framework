package it.smartcommunitylab.validationstorage.typed;

import java.io.Serializable;

public class ColumnField implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 5865549765364007263L;

    private String name;
    
    private FieldType type;
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public FieldType getType() {
        return type;
    }
    
    public void setType(FieldType type) {
        this.type = type;
    }
}

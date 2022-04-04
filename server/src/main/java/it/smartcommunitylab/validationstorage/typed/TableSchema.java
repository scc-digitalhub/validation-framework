package it.smartcommunitylab.validationstorage.typed;

import java.util.List;

public class TableSchema extends TypedSchema {
    /**
     * 
     */
    private static final long serialVersionUID = -8812097352804710997L;
    
    private List<ColumnField> fields;

    public List<ColumnField> getFields() {
        return fields;
    }

    public void setFields(List<ColumnField> fields) {
        this.fields = fields;
    }
}

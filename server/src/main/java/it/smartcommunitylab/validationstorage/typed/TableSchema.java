package it.smartcommunitylab.validationstorage.typed;

import java.util.List;

public class TableSchema extends TypedSchema {
    private List<ColumnField> fields;
    
    static class ColumnField {
        
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

    public List<ColumnField> getFields() {
        return fields;
    }

    public void setFields(List<ColumnField> fields) {
        this.fields = fields;
    }
}

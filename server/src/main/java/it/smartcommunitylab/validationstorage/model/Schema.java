package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Convert;
import javax.persistence.Embeddable;
import javax.persistence.Lob;
import javax.persistence.Transient;

import it.smartcommunitylab.validationstorage.converter.TypedSchemaConverter;
import it.smartcommunitylab.validationstorage.typed.TypedSchema;

@Embeddable
public class Schema {
    @Transient
    private String type;
    
    @Lob
    @Convert(converter = TypedSchemaConverter.class)
    private TypedSchema schema;

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public TypedSchema getSchema() {
        return schema;
    }

    public void setSchema(TypedSchema schema) {
        this.schema = schema;
    }

}

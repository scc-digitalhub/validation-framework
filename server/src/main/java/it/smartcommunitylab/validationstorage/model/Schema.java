package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;

import javax.persistence.Convert;
import javax.persistence.Embeddable;
import javax.persistence.Lob;
import javax.persistence.Transient;

import it.smartcommunitylab.validationstorage.converter.TypedSchemaConverter;
import it.smartcommunitylab.validationstorage.typed.TypedSchema;

@Embeddable
public class Schema implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = -172767736719219037L;

    @Transient
    private ResourceType type;
    
    @Lob
    @Convert(converter = TypedSchemaConverter.class)
    private TypedSchema schema;

    public ResourceType getType() {
        return type;
    }

    public void setType(ResourceType type) {
        this.type = type;
    }

    public TypedSchema getSchema() {
        return schema;
    }

    public void setSchema(TypedSchema schema) {
        this.schema = schema;
    }

}

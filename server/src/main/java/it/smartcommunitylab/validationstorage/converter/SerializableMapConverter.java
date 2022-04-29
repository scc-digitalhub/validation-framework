package it.smartcommunitylab.validationstorage.converter;

import java.io.Serializable;

public class SerializableMapConverter extends MapConverter<Serializable> {

    protected SerializableMapConverter() {
        super(Serializable.class);
    }
}

package it.smartcommunitylab.validationstorage.converter;

import it.smartcommunitylab.validationstorage.typed.TypedError;

public class TypedErrorListConverter extends ListConverter<TypedError> {

    protected TypedErrorListConverter() {
        super(TypedError.class);
    }
}
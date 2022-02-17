package it.smartcommunitylab.validationstorage.repository;

import java.util.Set;

import javax.persistence.AttributeConverter;

import org.springframework.util.StringUtils;

public class StringSetConverter implements AttributeConverter<Set<String>, String> {
    
    @Override
    public String convertToDatabaseColumn(Set<String> attribute) {
        return StringUtils.collectionToCommaDelimitedString(attribute);
    }

    @Override
    public Set<String> convertToEntityAttribute(String dbData) {
        return StringUtils.commaDelimitedListToSet(dbData);
    }

}
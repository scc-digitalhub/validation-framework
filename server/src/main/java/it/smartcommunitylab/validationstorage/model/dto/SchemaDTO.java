package it.smartcommunitylab.validationstorage.model.dto;

import javax.persistence.GeneratedValue;
import javax.persistence.Id;

public class SchemaDTO {
    @Id
    @GeneratedValue
    private long id;
    
    private long resourceId;
}

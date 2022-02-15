package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: schema of the data.
 */
public class ShortSchemaDTO {
    private long experimentId;
    
    private long runId;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;
    
}
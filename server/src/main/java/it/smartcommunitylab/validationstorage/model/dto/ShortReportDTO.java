package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: short report on the validation's result.
 */
public class ShortReportDTO {
    private long experimentId;
    
    private long runId;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;
    
}
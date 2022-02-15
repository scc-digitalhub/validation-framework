package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: details an experiment.
 */
@Valid
public class ExperimentDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private String title;
    
    private List<String> tags;
    
}

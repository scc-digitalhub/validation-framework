package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: details a project.
 */
@Valid
public class ProjectDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private String title;
    
}

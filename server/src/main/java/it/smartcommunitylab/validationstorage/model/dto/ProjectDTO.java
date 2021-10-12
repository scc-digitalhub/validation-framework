package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import lombok.Data;

/**
 * Request object: details a project.
 */
@Data
@Valid
public class ProjectDTO {
    /**
     * Unique ID.
     */
    @Pattern(regexp = ValidationStorageConstants.ID_PATTERN)
    @NotBlank
    private String id;

    /**
     * Name of the project.
     */
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
}

package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import lombok.Data;

/**
 * Request object: details an experiment.
 */
@Data
@Valid
public class ExperimentDTO {
    /**
     * ID of the experiment. Only unique within the project it belongs to.
     */
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.ID_PATTERN)
    private String experimentId;

    /**
     * Name of the experiment.
     */
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentName;
}

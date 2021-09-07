package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
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
    @Pattern(regexp = ValidationStorageUtils.ID_PATTERN)
    private String experimentId;

    /**
     * Name of the experiment.
     */
    @Pattern(regexp = ValidationStorageUtils.NAME_PATTERN)
    private String experimentName;
}

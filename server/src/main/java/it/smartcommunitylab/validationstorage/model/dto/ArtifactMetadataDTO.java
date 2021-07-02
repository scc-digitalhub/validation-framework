package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import lombok.Data;

/**
 * Request object: metadata about artifact files related to a run.
 */
@Data
@Valid
public class ArtifactMetadataDTO {
    /**
     * ID of the experiment this document belongs to.
     */
    @JsonProperty("experiment_id")
    @NotBlank
    @Pattern(regexp = ValidationStorageUtils.ID_PATTERN)
    private String experimentId;

    /**
     * Name of the experiment this document belongs to.
     */
    @JsonProperty("experiment_name")
    @Pattern(regexp = ValidationStorageUtils.NAME_PATTERN)
    private String experimentName;

    /**
     * ID of the run this document belongs to.
     */
    @JsonProperty("run_id")
    @NotBlank
    @Pattern(regexp = ValidationStorageUtils.ID_PATTERN)
    private String runId;

    /**
     * File name.
     */
    @NotBlank
    private String name;

    /**
     * File location.
     */
    @NotBlank
    private String uri;
}
package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;

/**
 * Request object: metadata about artifact files related to a run.
 */
@Valid
public class ArtifactMetadataDTO {
    private long experimentId;
    
    private long runId;

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
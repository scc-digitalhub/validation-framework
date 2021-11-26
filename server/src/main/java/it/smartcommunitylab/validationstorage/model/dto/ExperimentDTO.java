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
    
    /**
     * Tags.
     */
    private List<String> tags;

    public String getExperimentId() {
        return experimentId;
    }

    public void setExperimentId(String experimentId) {
        this.experimentId = experimentId;
    }

    public String getExperimentName() {
        return experimentName;
    }

    public void setExperimentName(String experimentName) {
        this.experimentName = experimentName;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    
    
}

package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: short report on the validation's result.
 */
public class RunEnvironmentDTO {
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String runId;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;

    public RunEnvironmentDTO() {
        contents = new HashMap<String, Serializable>();
    }

    @JsonAnyGetter
    public Map<String, Serializable> getContentMap() {
        return contents;
    }

    @JsonAnySetter
    public void addContent(String key, Serializable value) {
        contents.put(key, value);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getExperimentId() {
        return experimentId;
    }

    public void setExperimentId(String experimentId) {
        this.experimentId = experimentId;
    }

    public String getRunId() {
        return runId;
    }

    public void setRunId(String runId) {
        this.runId = runId;
    }

    public Map<String, Serializable> getContents() {
        return contents;
    }

    public void setContents(Map<String, Serializable> contents) {
        this.contents = contents;
    }

}
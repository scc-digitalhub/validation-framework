package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;

/**
 * Request object: short report on the validation's result.
 */
public class RunEnvironmentDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("experiment")
    private String experimentName;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("run")
    private String runId;
    
    private String datajudgeVersion;

    @JsonIgnore
    private Map<String, Serializable> contents;

    public RunEnvironmentDTO() {
        contents = new HashMap<String, Serializable>();
    }
    
    public static RunEnvironmentDTO from(RunEnvironment source, String experimentName) {
        if (source == null)
            return null;
        
        RunEnvironmentDTO dto = new RunEnvironmentDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentName(experimentName);
        dto.setRunId(source.getRunId());
        dto.setDatajudgeVersion(source.getDatajudgeVersion());
        
        if (source.getContents() != null)
            dto.setContents(source.getContents());
        
        return dto;
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

    public String getExperimentName() {
        return experimentName;
    }

    public void setExperimentName(String experimentName) {
        this.experimentName = experimentName;
    }

    public String getRunId() {
        return runId;
    }

    public void setRunId(String runId) {
        this.runId = runId;
    }
    
    public String getDatajudgeVersion() {
        return datajudgeVersion;
    }

    public void setDatajudgeVersion(String datajudgeVersion) {
        this.datajudgeVersion = datajudgeVersion;
    }

    public Map<String, Serializable> getContents() {
        return contents;
    }

    public void setContents(Map<String, Serializable> contents) {
        this.contents = contents;
    }

}
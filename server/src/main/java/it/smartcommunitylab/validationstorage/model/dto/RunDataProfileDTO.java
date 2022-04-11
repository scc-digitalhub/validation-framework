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
import it.smartcommunitylab.validationstorage.model.ReportMetadata;
import it.smartcommunitylab.validationstorage.model.RunDataProfile;

/**
 * Request object: profile for the data.
 */
public class RunDataProfileDTO {
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

    private String resourceName;
    
    private String type;
    
    private ReportMetadata metadata;
    
    @JsonIgnore
    private Map<String, Serializable> profile;

    public RunDataProfileDTO() {
        profile = new HashMap<String, Serializable>();
    }
    
    public static RunDataProfileDTO from(RunDataProfile source, String experimentName) {
        if (source == null)
            return null;
        
        RunDataProfileDTO dto = new RunDataProfileDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentName(experimentName);
        dto.setRunId(source.getRunId());
        dto.setResourceName(source.getResourceName());
        dto.setType(source.getType());
        dto.setMetadata(source.getMetadata());
        dto.setProfile(source.getProfile());
        
        return dto;
    }

    @JsonAnyGetter
    public Map<String, Serializable> getProfileMap() {
        return profile;
    }

    @JsonAnySetter
    public void addProfile(String key, Serializable value) {
        profile.put(key, value);
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

    public void setProjectId(String project) {
        this.projectId = project;
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

    public String getResourceName() {
        return resourceName;
    }

    public void setResourceName(String resourceName) {
        this.resourceName = resourceName;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public ReportMetadata getMetadata() {
        return metadata;
    }

    public void setMetadata(ReportMetadata metadata) {
        this.metadata = metadata;
    }

    public Map<String, Serializable> getProfile() {
        return profile;
    }

    public void setProfile(Map<String, Serializable> profile) {
        this.profile = profile;
    }

}
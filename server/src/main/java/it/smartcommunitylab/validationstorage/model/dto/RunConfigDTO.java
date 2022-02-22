package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

@Valid
public class RunConfigDTO {
    private String id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;
    
    private List<RunConfigImpl> snapshot;
    
    private List<RunConfigImpl> profiling;
    
    private List<RunConfigImpl> schemaInference;
    
    private List<RunConfigImpl> validation;
    
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

    public List<RunConfigImpl> getSnapshot() {
        return snapshot;
    }

    public void setSnapshot(List<RunConfigImpl> snapshot) {
        this.snapshot = snapshot;
    }

    public List<RunConfigImpl> getProfiling() {
        return profiling;
    }

    public void setProfiling(List<RunConfigImpl> profiling) {
        this.profiling = profiling;
    }

    public List<RunConfigImpl> getSchemaInference() {
        return schemaInference;
    }

    public void setSchemaInference(List<RunConfigImpl> schemaInference) {
        this.schemaInference = schemaInference;
    }

    public List<RunConfigImpl> getValidation() {
        return validation;
    }

    public void setValidation(List<RunConfigImpl> validation) {
        this.validation = validation;
    }
    
}

package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

@Valid
public class RunConfigDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;
    
    private RunConfigImpl snapshot;
    
    private RunConfigImpl profiling;
    
    private RunConfigImpl schemaInference;
    
    private RunConfigImpl validation;

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

    public RunConfigImpl getSnapshot() {
        return snapshot;
    }

    public void setSnapshot(RunConfigImpl snapshot) {
        this.snapshot = snapshot;
    }

    public RunConfigImpl getProfiling() {
        return profiling;
    }

    public void setProfiling(RunConfigImpl profiling) {
        this.profiling = profiling;
    }

    public RunConfigImpl getSchemaInference() {
        return schemaInference;
    }

    public void setSchemaInference(RunConfigImpl schemaInference) {
        this.schemaInference = schemaInference;
    }

    public RunConfigImpl getValidation() {
        return validation;
    }

    public void setValidation(RunConfigImpl validation) {
        this.validation = validation;
    }
    
}

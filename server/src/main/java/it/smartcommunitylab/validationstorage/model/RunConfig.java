package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Column;
import javax.persistence.Embedded;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Entity
public class RunConfig {
    @Id
    @GeneratedValue
    private long id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "experiment_id")
    private String experimentId;
    
    @Embedded
    private RunConfigImpl snapshot;
    
    @Embedded
    private RunConfigImpl profiling;
    
    @Embedded
    private RunConfigImpl schemaInference;
    
    @Embedded
    private RunConfigImpl validation;

    public long getId() {
        return id;
    }

    public void setId(long id) {
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

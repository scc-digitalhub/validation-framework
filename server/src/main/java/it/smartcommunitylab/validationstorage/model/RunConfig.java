package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.converter.RunConfigImplListConverter;

@Entity
@Table(name = "configs")
public class RunConfig {
    @Id
    private String id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "experiment_id")
    private String experimentId;
    
    @Lob
    @Convert(converter = RunConfigImplListConverter.class)
    private List<RunConfigImpl> snapshot;
    
    @Lob
    @Convert(converter = RunConfigImplListConverter.class)
    private List<RunConfigImpl> profiling;
    
    @Lob
    @Convert(converter = RunConfigImplListConverter.class)
    private List<RunConfigImpl> schemaInference;
    
    @Lob
    @Convert(converter = RunConfigImplListConverter.class)
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
    
    public boolean isValidationEnabled() {
        return validation != null && !validation.isEmpty();
    }
    
}

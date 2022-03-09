package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Collections;
import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

@Valid
@JsonInclude(Include.NON_NULL)
public class RunConfigDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    private List<RunConfigImpl> snapshot;

    private List<RunConfigImpl> profiling;

    @JsonProperty("inference")
    private List<RunConfigImpl> schemaInference;

    private List<RunConfigImpl> validation;

    public RunConfigDTO() {
        snapshot = Collections.<RunConfigImpl>emptyList();
        profiling = Collections.<RunConfigImpl>emptyList();
        schemaInference = Collections.<RunConfigImpl>emptyList();
        validation = Collections.<RunConfigImpl>emptyList();
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

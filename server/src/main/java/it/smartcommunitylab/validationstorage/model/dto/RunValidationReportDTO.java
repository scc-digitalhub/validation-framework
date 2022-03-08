package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;
import it.smartcommunitylab.validationstorage.typed.TypedError;

/**
 * Request object: short report on the validation's result.
 */
public class RunValidationReportDTO {
    private String id;
    
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;
    
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String runId;
    
    private String type;
    
    private TypedConstraint constraint;
    
    @NotNull
    private Boolean valid;
    
    List<TypedError> errors;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;
    
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
    
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
    
    public TypedConstraint getConstraint() {
        return constraint;
    }

    public void setConstraint(TypedConstraint constraint) {
        this.constraint = constraint;
    }

    public boolean isValid() {
        return valid != null ? valid.booleanValue() : false;
    }

    public Boolean getValid() {
        return valid;
    }

    public void setValid(Boolean valid) {
        this.valid = valid;
    }
    
    public List<TypedError> getErrors() {
        return errors;
    }
    
    public void setErrors(List<TypedError> errors) {
        this.errors = errors;
    }
    
    public Map<String, Serializable> getContents() {
        return contents;
    }

    public void setContents(Map<String, Serializable> contents) {
        this.contents = contents;
    }
    
}
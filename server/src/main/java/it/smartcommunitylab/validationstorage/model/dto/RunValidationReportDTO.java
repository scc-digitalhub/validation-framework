package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.ReportMetadata;
import it.smartcommunitylab.validationstorage.model.RunValidationReport;
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

    private String constraintName;

    @NotNull
    private Boolean valid;
    
    private ReportMetadata metadata;

    List<TypedError> errors;
    
    private Map<String, Serializable> contents;

    public RunValidationReportDTO() {
        contents = new HashMap<String, Serializable>();
    }
    
    public static RunValidationReportDTO from(RunValidationReport source) {
        if (source == null)
            return null;
        
        RunValidationReportDTO dto = new RunValidationReportDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setRunId(source.getRunId());
        dto.setType(source.getType());
        dto.setConstraintName(source.getConstraintName());
        dto.setValid(source.getValid());
        dto.setMetadata(source.getMetadata());
        dto.setErrors(source.getErrors());
        
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

    public String getConstraintName() {
        return constraintName;
    }

    public void setConstraintName(String constraintName) {
        this.constraintName = constraintName;
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

    public ReportMetadata getMetadata() {
        return metadata;
    }

    public void setMetadata(ReportMetadata metadata) {
        this.metadata = metadata;
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
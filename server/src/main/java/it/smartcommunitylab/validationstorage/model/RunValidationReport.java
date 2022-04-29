package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.Embedded;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.converter.SerializableMapConverter;
import it.smartcommunitylab.validationstorage.converter.TypedErrorListConverter;
import it.smartcommunitylab.validationstorage.typed.TypedError;

/**
 * Short report on the validation's result.
 */
@Entity
@Table(name = "run_validation_reports")
public class RunValidationReport {
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

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "run_id")
    private String runId;

    private String type;

    @Column(name = "constraint_name")
    private String constraintName;

    private Boolean valid;

    @Embedded
    @Column(name = "metadata")
    private ReportMetadata metadata;

    @Lob
    @Convert(converter = TypedErrorListConverter.class)
    List<TypedError> errors;
    
    @Lob
    @Convert(converter = SerializableMapConverter.class)
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

    public String getConstraintName() {
        return constraintName;
    }

    public void setConstraintName(String constraintName) {
        this.constraintName = constraintName;
    }

    public Boolean getValid() {
        return valid;
    }

    public void setValid(Boolean valid) {
        this.valid = valid;
    }

    public boolean isValid() {
        return valid != null ? valid.booleanValue() : false;
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
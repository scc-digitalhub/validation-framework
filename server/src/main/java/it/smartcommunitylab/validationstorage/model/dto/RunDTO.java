package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;
import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Valid
public class RunDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private long experimentId;
    
    private long packageId;
    
    private long runConfigId;
    
    private Map<String, Serializable> constraints;
    
    private long runMetadataId;
    
    private long runEnvironmentId;
    
    private Set<Long> artifactMetadataIds;
    
    private Set<Long> runDataProfileIds;
    
    private Set<Long> runDataResourceIds;
    
    private Set<Long> runShortReportIds;
    
    private Set<Long> runShortSchemaIds;

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public long getExperimentId() {
        return experimentId;
    }

    public void setExperimentId(long experimentId) {
        this.experimentId = experimentId;
    }

    public long getPackageId() {
        return packageId;
    }

    public void setPackageId(long packageId) {
        this.packageId = packageId;
    }

    public long getRunConfigId() {
        return runConfigId;
    }

    public void setRunConfigId(long runConfigId) {
        this.runConfigId = runConfigId;
    }

    public Map<String, Serializable> getConstraints() {
        return constraints;
    }

    public void setConstraints(Map<String, Serializable> constraints) {
        this.constraints = constraints;
    }

    public long getRunMetadataId() {
        return runMetadataId;
    }

    public void setRunMetadataId(long runMetadataId) {
        this.runMetadataId = runMetadataId;
    }

    public long getRunEnvironmentId() {
        return runEnvironmentId;
    }

    public void setRunEnvironmentId(long runEnvironmentId) {
        this.runEnvironmentId = runEnvironmentId;
    }

    public Set<Long> getArtifactMetadataIds() {
        return artifactMetadataIds;
    }

    public void setArtifactMetadataIds(Set<Long> artifactMetadataIds) {
        this.artifactMetadataIds = artifactMetadataIds;
    }

    public Set<Long> getRunDataProfileIds() {
        return runDataProfileIds;
    }

    public void setRunDataProfileIds(Set<Long> runDataProfileIds) {
        this.runDataProfileIds = runDataProfileIds;
    }

    public Set<Long> getRunDataResourceIds() {
        return runDataResourceIds;
    }

    public void setRunDataResourceIds(Set<Long> runDataResourceIds) {
        this.runDataResourceIds = runDataResourceIds;
    }

    public Set<Long> getRunShortReportIds() {
        return runShortReportIds;
    }

    public void setRunShortReportIds(Set<Long> runShortReportIds) {
        this.runShortReportIds = runShortReportIds;
    }

    public Set<Long> getRunShortSchemaIds() {
        return runShortSchemaIds;
    }

    public void setRunShortSchemaIds(Set<Long> runShortSchemaIds) {
        this.runShortSchemaIds = runShortSchemaIds;
    }
    
}

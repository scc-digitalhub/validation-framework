package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Valid
public class RunDTO {
    private String projectId;
    
    private long experimentId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private long packageId;
    
    private long runConfigId;
    
    private long[] constraints;
    
    private long runDataProfileId;
    
    private long runDataResourceId;
    
    private long runEnvironmentId;
    
    private long runMetadataId;
    
    private long runShortReportId;
    
    private long runShortSchemaId;

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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
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

    public long[] getConstraints() {
        return constraints;
    }

    public void setConstraints(long[] constraints) {
        this.constraints = constraints;
    }

    public long getRunDataProfileId() {
        return runDataProfileId;
    }

    public void setRunDataProfileId(long runDataProfileId) {
        this.runDataProfileId = runDataProfileId;
    }

    public long getRunDataResourceId() {
        return runDataResourceId;
    }

    public void setRunDataResourceId(long runDataResourceId) {
        this.runDataResourceId = runDataResourceId;
    }

    public long getRunEnvironmentId() {
        return runEnvironmentId;
    }

    public void setRunEnvironmentId(long runEnvironmentId) {
        this.runEnvironmentId = runEnvironmentId;
    }

    public long getRunMetadataId() {
        return runMetadataId;
    }

    public void setRunMetadataId(long runMetadataId) {
        this.runMetadataId = runMetadataId;
    }

    public long getRunShortReportId() {
        return runShortReportId;
    }

    public void setRunShortReportId(long runShortReportId) {
        this.runShortReportId = runShortReportId;
    }

    public long getRunShortSchemaId() {
        return runShortSchemaId;
    }

    public void setRunShortSchemaId(long runShortSchemaId) {
        this.runShortSchemaId = runShortSchemaId;
    }
    
}

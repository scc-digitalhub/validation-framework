package it.smartcommunitylab.validationstorage.model;

import java.util.Date;
import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Valid
public class RunSummary {
    
    @NotNull
    private String id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.ID_PATTERN)
    private String projectId;
    
    @NotNull
    private String experimentId;
    
    @NotNull
    private String runId;
    
    @NotNull
    private Date created;

    private List<ArtifactMetadata> artifactMetadata;

    private RunDataProfile dataProfile;

    private RunDataResource dataResource;

    private RunEnvironment runEnvironment;

    private RunMetadata runMetadata;

    private RunValidationReport shortReport;

    private RunDataSchema shortSchema;

    public RunSummary(String id, String projectId, String experimentId, String runId, Date created) {
        this.id = id;
        this.projectId = projectId;
        this.experimentId = experimentId;
        this.runId = runId;
        this.created = created;
    }

    public String getId() {
        return id;
    }

    public String getProjectId() {
        return projectId;
    }

    public String getExperimentId() {
        return experimentId;
    }

    public String getRunId() {
        return runId;
    }

    public Date getCreated() {
        return created;
    }

    public List<ArtifactMetadata> getArtifactMetadata() {
        return artifactMetadata;
    }
    
    public void setArtifactMetadata(List<ArtifactMetadata> artifactMetadata) {
        this.artifactMetadata = artifactMetadata;
    }

    public RunDataProfile getDataProfile() {
        return dataProfile;
    }
    
    public void setDataProfile(RunDataProfile dataProfile) {
        this.dataProfile = dataProfile;
    }

    public RunDataResource getDataResource() {
        return dataResource;
    }
    
    public void setDataResource(RunDataResource dataResource) {
        this.dataResource = dataResource;
    }

    public RunEnvironment getRunEnvironment() {
        return runEnvironment;
    }
    
    public void setRunEnvironment(RunEnvironment runEnvironment) {
        this.runEnvironment = runEnvironment;
    }

    public RunMetadata getRunMetadata() {
        return runMetadata;
    }
    
    public void setRunMetadata(RunMetadata runMetadata) {
        this.runMetadata = runMetadata;
    }

    public RunValidationReport getShortReport() {
        return shortReport;
    }
    
    public void setShortReport(RunValidationReport shortReport) {
        this.shortReport = shortReport;
    }

    public RunDataSchema getShortSchema() {
        return shortSchema;
    }
    
    public void setShortSchema(RunDataSchema shortSchema) {
        this.shortSchema = shortSchema;
    }
    
}

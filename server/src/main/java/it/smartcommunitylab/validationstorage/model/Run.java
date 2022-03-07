package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Lob;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.repository.HashMapConverter;

@Entity
public class Run {
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
    
    @OneToOne()
    @Column(name = "run_config")
    private RunConfig runConfig;
    
    @Lob
    @Convert(converter = HashMapConverter.class)
    private Map<String, Serializable> constraints;
    
    @OneToOne()
    @Column(name = "run_metadata")
    private RunMetadata runMetadata;
    
    @OneToOne()
    @Column(name = "run_environment")
    private RunEnvironment runEnvironment;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    private List<ArtifactMetadata> artifactMetadata;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "run_data_profiles")
    private List<RunDataProfile> runDataProfiles;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "run_validation_reports")
    private List<RunValidationReport> runValiationReports;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "run_data_schemas")
    private List<RunDataSchema> runDataSchemas;
    
    private String status;
    
    private String validationResult;
    
    private String profileResult;
    
    private String schemaResult;
    
    private String snapshotResult;

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

    public RunConfig getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfig runConfig) {
        this.runConfig = runConfig;
    }

    public Map<String, Serializable> getConstraints() {
        return constraints;
    }

    public void setConstraints(Map<String, Serializable> constraints) {
        this.constraints = constraints;
    }

    public RunMetadata getRunMetadata() {
        return runMetadata;
    }

    public void setRunMetadata(RunMetadata runMetadata) {
        this.runMetadata = runMetadata;
    }

    public RunEnvironment getRunEnvironment() {
        return runEnvironment;
    }

    public void setRunEnvironment(RunEnvironment runEnvironment) {
        this.runEnvironment = runEnvironment;
    }

    public List<ArtifactMetadata> getArtifactMetadata() {
        return artifactMetadata;
    }

    public void setArtifactMetadata(List<ArtifactMetadata> artifactMetadata) {
        this.artifactMetadata = artifactMetadata;
    }

    public List<RunDataProfile> getRunDataProfiles() {
        return runDataProfiles;
    }

    public void setRunDataProfiles(List<RunDataProfile> runDataProfiles) {
        this.runDataProfiles = runDataProfiles;
    }

    public List<RunValidationReport> getRunValidationReports() {
        return runValiationReports;
    }

    public void setRunValidationReports(List<RunValidationReport> runValiationReports) {
        this.runValiationReports = runValiationReports;
    }

    public List<RunDataSchema> getRunDataSchemas() {
        return runDataSchemas;
    }

    public void setRunDataSchemas(List<RunDataSchema> runDataSchemas) {
        this.runDataSchemas = runDataSchemas;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getValidationResult() {
        return validationResult;
    }

    public void setValidationResult(String validationResult) {
        this.validationResult = validationResult;
    }

    public String getProfileResult() {
        return profileResult;
    }

    public void setProfileResult(String profileResult) {
        this.profileResult = profileResult;
    }

    public String getSchemaResult() {
        return schemaResult;
    }

    public void setSchemaResult(String schemaResult) {
        this.schemaResult = schemaResult;
    }

    public String getSnapshotResult() {
        return snapshotResult;
    }

    public void setSnapshotResult(String snapshotResult) {
        this.snapshotResult = snapshotResult;
    }

}

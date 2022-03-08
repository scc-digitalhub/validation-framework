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
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.converter.HashMapConverter;

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
    
    // Copied from the experiment's current RunConfig, cannot be modified
    @OneToOne
    @Column(name = "run_config")
    private RunConfig runConfig;
    
    // Copied from the experiment's package, cannot be modified
    @OneToOne
    @Column(name = "data_package")
    private DataPackage dataPackage;
    
    @Lob
    @Convert(converter = HashMapConverter.class)
    private Map<String, Serializable> constraints;
    
    @NotNull
    @Column(name = "run_status")
    private RunResult runStatus;
    
    // These documents are populated as results are obtained
    @OneToOne()
    @Column(name = "run_metadata")
    private RunMetadata runMetadata;
    
    @OneToOne()
    @Column(name = "run_environment")
    private RunEnvironment runEnvironment;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "artifact_metadata")
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
    
    @Column(name = "validation_result")
    private RunResult validationResult;
    
    @Column(name = "profile_result")
    private RunResult profileResult;
    
    @Column(name = "schema_result")
    private RunResult schemaResult;
    
    @Column(name = "snapshot_result")
    private RunResult snapshotResult;
    
    public enum RunResult {
        PENDING("pending"),
        RUNNING("running"),
        SUCCESS("success"),
        ERROR("error");
        
        public final String label;
        
        private RunResult(String label) {
            this.label = label;
        }
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

    public RunConfig getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfig runConfig) {
        this.runConfig = runConfig;
    }

    public DataPackage getDataPackage() {
        return dataPackage;
    }

    public void setDataPackage(DataPackage dataPackage) {
        this.dataPackage = dataPackage;
    }

    public Map<String, Serializable> getConstraints() {
        return constraints;
    }

    public void setConstraints(Map<String, Serializable> constraints) {
        this.constraints = constraints;
    }

    public RunResult getRunStatus() {
        return runStatus;
    }

    public void setRunStatus(RunResult runStatus) {
        this.runStatus = runStatus;
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

    public List<RunValidationReport> getRunValiationReports() {
        return runValiationReports;
    }

    public void setRunValiationReports(List<RunValidationReport> runValiationReports) {
        this.runValiationReports = runValiationReports;
    }

    public List<RunDataSchema> getRunDataSchemas() {
        return runDataSchemas;
    }

    public void setRunDataSchemas(List<RunDataSchema> runDataSchemas) {
        this.runDataSchemas = runDataSchemas;
    }

    public RunResult getValidationResult() {
        return validationResult;
    }

    public void setValidationResult(RunResult validationResult) {
        this.validationResult = validationResult;
    }

    public RunResult getProfileResult() {
        return profileResult;
    }

    public void setProfileResult(RunResult profileResult) {
        this.profileResult = profileResult;
    }

    public RunResult getSchemaResult() {
        return schemaResult;
    }

    public void setSchemaResult(RunResult schemaResult) {
        this.schemaResult = schemaResult;
    }

    public RunResult getSnapshotResult() {
        return snapshotResult;
    }

    public void setSnapshotResult(RunResult snapshotResult) {
        this.snapshotResult = snapshotResult;
    }

    

}

package it.smartcommunitylab.validationstorage.model;

import java.util.List;
import java.util.Map;

import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Lob;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.converter.HashMapConverter;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;

@Entity
@Table(name = "runs")
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

    // Key is resource's name
    @Lob
    @Convert(converter = HashMapConverter.class)
    private Map<String, DataResource> resources;

    // Key is constraint's name
    @Lob
    @Convert(converter = HashMapConverter.class)
    private Map<String, TypedConstraint> constraints;

    @NotNull
    @Column(name = "run_status")
    private RunStatus runStatus;

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
    private RunStatus validationResult;

    @Column(name = "profile_result")
    private RunStatus profileResult;

    @Column(name = "schema_result")
    private RunStatus schemaResult;

    @Column(name = "snapshot_result")
    private RunStatus snapshotResult;

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

    public Map<String, DataResource> getResources() {
        return resources;
    }

    public void setResources(Map<String, DataResource> resources) {
        this.resources = resources;
    }

    public Map<String, TypedConstraint> getConstraints() {
        return constraints;
    }

    public void setConstraints(Map<String, TypedConstraint> constraints) {
        this.constraints = constraints;
    }

    public RunStatus getRunStatus() {
        return runStatus;
    }

    public void setRunStatus(RunStatus runStatus) {
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

    public RunStatus getValidationResult() {
        return validationResult;
    }

    public void setValidationResult(RunStatus validationResult) {
        this.validationResult = validationResult;
    }

    public RunStatus getProfileResult() {
        return profileResult;
    }

    public void setProfileResult(RunStatus profileResult) {
        this.profileResult = profileResult;
    }

    public RunStatus getSchemaResult() {
        return schemaResult;
    }

    public void setSchemaResult(RunStatus schemaResult) {
        this.schemaResult = schemaResult;
    }

    public RunStatus getSnapshotResult() {
        return snapshotResult;
    }

    public void setSnapshotResult(RunStatus snapshotResult) {
        this.snapshotResult = snapshotResult;
    }

}

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
    @Column(name = "run_data_profile")
    private List<RunDataProfile> runDataProfiles;
    
    @OneToMany(mappedBy="run_id")
    @Column(name = "run_data_resources")
    private List<RunDataResource> runDataResources;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "run_short_report")
    private List<RunShortReport> runShortReports;
    
    @OneToMany(mappedBy = "run_id", fetch = FetchType.LAZY)
    @Column(name = "run_short_schema")
    private List<RunShortSchema> runShortSchemas;
    
    private String status;
    
    private Boolean valid;

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

    public List<RunDataResource> getRunDataResources() {
        return runDataResources;
    }

    public void setRunDataResources(List<RunDataResource> runDataResources) {
        this.runDataResources = runDataResources;
    }

    public List<RunShortReport> getRunShortReports() {
        return runShortReports;
    }

    public void setRunShortReports(List<RunShortReport> runShortReports) {
        this.runShortReports = runShortReports;
    }

    public List<RunShortSchema> getRunShortSchemas() {
        return runShortSchemas;
    }

    public void setRunShortSchemas(List<RunShortSchema> runShortSchemas) {
        this.runShortSchemas = runShortSchemas;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Boolean getValid() {
        return valid;
    }

    public void setValid(Boolean valid) {
        this.valid = valid;
    }

}

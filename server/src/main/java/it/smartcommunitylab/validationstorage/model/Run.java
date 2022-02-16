package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Entity
@Table(name = "run", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "experiment_name", "name" }))
public class Run {
    @Id
    @GeneratedValue
    private long id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "experiment_name")
    private String experimentName;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    @OneToMany(mappedBy = "runName", fetch = FetchType.LAZY)
    private List<ArtifactMetadata> artifactMetadata;
    
    @OneToOne()
    private RunDataProfile runDataProfile;
    
    @OneToOne()
    private RunDataResource runDataResource;
    
    @OneToOne()
    private RunEnvironment runEnvironment;
    
    @OneToOne()
    private RunMetadata runMetadata;
    
    @OneToOne()
    private RunShortReport runShortReport;
    
    @OneToOne()
    private RunShortSchema runShortSchema;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getExperimentName() {
        return experimentName;
    }

    public void setExperimentName(String experimentName) {
        this.experimentName = experimentName;
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

    public List<ArtifactMetadata> getArtifactMetadata() {
        return artifactMetadata;
    }

    public void setArtifactMetadata(List<ArtifactMetadata> artifactMetadata) {
        this.artifactMetadata = artifactMetadata;
    }

    public RunDataProfile getRunDataProfile() {
        return runDataProfile;
    }

    public void setRunDataProfile(RunDataProfile runDataProfile) {
        this.runDataProfile = runDataProfile;
    }

    public RunDataResource getRunDataResource() {
        return runDataResource;
    }

    public void setRunDataResource(RunDataResource runDataResource) {
        this.runDataResource = runDataResource;
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

    public RunShortReport getRunShortReport() {
        return runShortReport;
    }

    public void setRunShortReport(RunShortReport runShortReport) {
        this.runShortReport = runShortReport;
    }

    public RunShortSchema getRunShortSchema() {
        return runShortSchema;
    }

    public void setRunShortSchema(RunShortSchema runShortSchema) {
        this.runShortSchema = runShortSchema;
    }
    
}

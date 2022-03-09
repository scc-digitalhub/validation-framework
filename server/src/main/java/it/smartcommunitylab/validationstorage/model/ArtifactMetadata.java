package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Metadata about artifact files related to a run.
 */
@Entity
@Table(name = "artifact_metadata")
public class ArtifactMetadata {
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

    /**
     * File name.
     */
    private String name;

    /**
     * File location.
     */
    private String uri;

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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        this.uri = uri;
    }
    
}
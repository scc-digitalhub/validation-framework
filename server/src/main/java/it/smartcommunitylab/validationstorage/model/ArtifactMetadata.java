package it.smartcommunitylab.validationstorage.model;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Metadata about artifact files related to a run.
 */
@Valid
@Document
public class ArtifactMetadata {
    /**
     * Unique ID of this document.
     */
    @Id
    private String id;

    /**
     * ID of the project this document belongs to.
     */
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.ID_PATTERN)
    private String projectId;

    /**
     * ID of the experiment this document belongs to.
     */
    private String experimentId;

    /**
     * ID of the run this document belongs to.
     */
    private String runId;

    /**
     * File name.
     */
    private String name;

    /**
     * File location.
     */
    private String uri;
    
    /**
     * Name of the experiment this document belongs to.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;
    
    public ArtifactMetadata(String projectId, String experimentId, String runId, String name, String uri) {
        this.projectId = projectId;
        this.experimentId = experimentId;
        this.runId = runId;
        this.name = name;
        this.uri = uri;
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

    public String getExperimentName() {
        return experimentName;
    }

    public void setExperimentName(String experimentName) {
        this.experimentName = experimentName;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
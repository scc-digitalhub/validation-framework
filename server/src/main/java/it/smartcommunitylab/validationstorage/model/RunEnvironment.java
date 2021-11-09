package it.smartcommunitylab.validationstorage.model;

import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Short report on the validation's result.
 */
@Valid
@Document
public class RunEnvironment {
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
     * Name of the experiment this document belongs to.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;

    /**
     * May contain extra information.
     */
    private Map<String, ?> contents;

    public RunEnvironment(String projectId, String experimentId, String runId) {
        this.projectId = projectId;
        this.experimentId = experimentId;
        this.runId = runId;
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

    public Map<String, ?> getContents() {
        return contents;
    }

    public void setContents(Map<String, ?> contents) {
        this.contents = contents;
    }
    
}
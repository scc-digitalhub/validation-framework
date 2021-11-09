package it.smartcommunitylab.validationstorage.model;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Details an experiment.
 */
@Valid
@Document
public class Experiment {
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
     * ID of the experiment. Only unique within the project it belongs to.
     */
    private String experimentId;

    /**
     * Name of the experiment.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;

    public Experiment(String projectId, String experimentId) {
        this.projectId = projectId;
        this.experimentId = experimentId;
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

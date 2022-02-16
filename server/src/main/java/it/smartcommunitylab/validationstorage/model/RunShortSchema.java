package it.smartcommunitylab.validationstorage.model;

import java.util.Map;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Schema of the data.
 */
@Entity
@Table(name = "run_short_schema", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "experiment_name", "run_name" }))
public class RunShortSchema {
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
    @Column(name = "run_name")
    private String runName;

    /**
     * May contain extra information.
     */
    private Map<String, ?> contents;

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

    public String getRunName() {
        return runName;
    }

    public void setRunName(String runName) {
        this.runName = runName;
    }

    public Map<String, ?> getContents() {
        return contents;
    }

    public void setContents(Map<String, ?> contents) {
        this.contents = contents;
    }
    
}
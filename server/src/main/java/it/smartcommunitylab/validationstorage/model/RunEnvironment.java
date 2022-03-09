package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.Map;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Short report on the validation's result.
 */
@Entity
@Table(name = "run_environments", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "experiment_name",
        "run_name" }))
public class RunEnvironment {
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

    @Column(name = "datajudge_version")
    private String datajudgeVersion;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;

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

    public String getDatajudgeVersion() {
        return datajudgeVersion;
    }

    public void setDatajudgeVersion(String datajudgeVersion) {
        this.datajudgeVersion = datajudgeVersion;
    }

    public Map<String, Serializable> getContents() {
        return contents;
    }

    public void setContents(Map<String, Serializable> contents) {
        this.contents = contents;
    }

}
package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: details an experiment.
 */
@Valid
public class ExperimentDTO {
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private long[] runs;
    
    private long runConfig;
    
    private long[] resources;

    private long[] constraints;
    
    private List<String> tags;

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
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

    public long[] getRuns() {
        return runs;
    }

    public void setRuns(long[] runs) {
        this.runs = runs;
    }

    public long getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(long runConfig) {
        this.runConfig = runConfig;
    }

    public long[] getResources() {
        return resources;
    }

    public void setResources(long[] resources) {
        this.resources = resources;
    }

    public long[] getConstraints() {
        return constraints;
    }

    public void setConstraints(long[] constraints) {
        this.constraints = constraints;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    
}

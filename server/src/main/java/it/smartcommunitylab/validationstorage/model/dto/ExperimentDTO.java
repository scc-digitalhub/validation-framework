package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: details an experiment.
 */
@Valid
public class ExperimentDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private Set<String> runs;
    
    private Set<Long> runConfigIds;
    
    private Set<Long> resourceIds;

    private Set<Long> constraintIds;
    
    private Set<String> tags;

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

    public Set<String> getRuns() {
        return runs;
    }

    public void setRuns(Set<String> runs) {
        this.runs = runs;
    }

    public Set<Long> getRunConfigIds() {
        return runConfigIds;
    }

    public void setRunConfigIds(Set<Long> runConfigIds) {
        this.runConfigIds = runConfigIds;
    }

    public Set<Long> getResourceIds() {
        return resourceIds;
    }

    public void setResourceIds(Set<Long> resourceIds) {
        this.resourceIds = resourceIds;
    }

    public Set<Long> getConstraintIds() {
        return constraintIds;
    }

    public void setConstraintIds(Set<Long> constraintIds) {
        this.constraintIds = constraintIds;
    }

    public Set<String> getTags() {
        return tags;
    }

    public void setTags(Set<String> tags) {
        this.tags = tags;
    }
    
}

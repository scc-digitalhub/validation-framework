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
    private String id;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private String description;
    
    private Set<String> runIds;
    
    private Set<String> runConfigIds;
    
    private Set<String> resourceIds;

    private Set<String> constraintIds;
    
    private Set<String> tags;
    
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
    
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Set<String> getRunIds() {
        return runIds;
    }

    public void setRunIds(Set<String> runIds) {
        this.runIds = runIds;
    }

    public Set<String> getRunConfigIds() {
        return runConfigIds;
    }

    public void setRunConfigIds(Set<String> runConfigIds) {
        this.runConfigIds = runConfigIds;
    }

    public Set<String> getResourceIds() {
        return resourceIds;
    }

    public void setResourceIds(Set<String> resourceIds) {
        this.resourceIds = resourceIds;
    }

    public Set<String> getConstraintIds() {
        return constraintIds;
    }

    public void setConstraintIds(Set<String> constraintIds) {
        this.constraintIds = constraintIds;
    }

    public Set<String> getTags() {
        return tags;
    }

    public void setTags(Set<String> tags) {
        this.tags = tags;
    }
    
}

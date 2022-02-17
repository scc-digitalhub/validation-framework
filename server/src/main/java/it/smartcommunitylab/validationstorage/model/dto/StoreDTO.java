package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;
import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Valid
public class StoreDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;
    
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private String path;
    
    private Map<String, Serializable> config;
    
    private boolean isDefault;
    
    private Set<Long> resources;

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

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public Map<String, Serializable> getConfig() {
        return config;
    }

    public void setConfig(Map<String, Serializable> config) {
        this.config = config;
    }

    public boolean isDefault() {
        return isDefault;
    }

    public void setDefault(boolean isDefault) {
        this.isDefault = isDefault;
    }

    public Set<Long> getResources() {
        return resources;
    }

    public void setResources(Set<Long> resources) {
        this.resources = resources;
    }
    
}

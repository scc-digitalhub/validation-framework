package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Store;

@Valid
public class StoreDTO {
    private String id;
    
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private String uri;

    private Map<String, Serializable> config;

    private Boolean isDefault;
    
    public static StoreDTO from(Store source) {
        if (source == null)
            return null;
        
        StoreDTO dto = new StoreDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setUri(source.getUri());
        dto.setConfig(source.getConfig());
        dto.setIsDefault(source.getIsDefault());
        
        return dto;
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

    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        this.uri = uri;
    }

    public Map<String, Serializable> getConfig() {
        return config;
    }

    public void setConfig(Map<String, Serializable> config) {
        this.config = config;
    }

    public Boolean getIsDefault() {
        return isDefault;
    }

    public void setIsDefault(Boolean isDefault) {
        this.isDefault = isDefault;
    }

    public boolean isDefault() {
        return isDefault != null ? isDefault.booleanValue() : false;
    }

}

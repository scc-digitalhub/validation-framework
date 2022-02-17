package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Request object: details a project.
 */
@Valid
public class ProjectDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private String description;
    
    private Set<String> experimentIds;
    
    private Set<Long> packageIds;
    
    private Set<Long> storeIds;

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

    public Set<String> getExperimentIds() {
        return experimentIds;
    }

    public void setExperimentIds(Set<String> experimentIds) {
        this.experimentIds = experimentIds;
    }

    public Set<Long> getPackageIds() {
        return packageIds;
    }

    public void setPackageIds(Set<Long> packageIds) {
        this.packageIds = packageIds;
    }

    public Set<Long> getStoreIds() {
        return storeIds;
    }

    public void setStoreIds(Set<Long> storeIds) {
        this.storeIds = storeIds;
    }
    
}

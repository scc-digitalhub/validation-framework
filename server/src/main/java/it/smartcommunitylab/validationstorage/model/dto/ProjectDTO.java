package it.smartcommunitylab.validationstorage.model.dto;

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
    
    private long[] experiments;
    
    private long[] dataPackages;
    
    private long[] stores;

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

    public long[] getExperiments() {
        return experiments;
    }

    public void setExperiments(long[] experiments) {
        this.experiments = experiments;
    }

    public long[] getDataPackages() {
        return dataPackages;
    }

    public void setDataPackages(long[] dataPackages) {
        this.dataPackages = dataPackages;
    }

    public long[] getStores() {
        return stores;
    }

    public void setStores(long[] stores) {
        this.stores = stores;
    }
    
}

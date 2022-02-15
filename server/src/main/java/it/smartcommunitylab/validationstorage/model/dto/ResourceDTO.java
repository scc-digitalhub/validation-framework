package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Resource.Dataset;
import it.smartcommunitylab.validationstorage.model.Schema;

@Valid
public class ResourceDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private String title;
    
    private String path;
    
    private long storeId;
    
    private long dataPackageId;
    
    private Schema schema;
    
    private Dataset dataset;
}

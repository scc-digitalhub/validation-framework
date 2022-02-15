package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Valid
public class StoreDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private String title;
    
    private String path;
    
    private Map<String, ?> config;
    
    private boolean isDefault = false;
}

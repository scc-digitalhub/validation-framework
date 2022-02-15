package it.smartcommunitylab.validationstorage.model.dto;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

@Valid
public class RunConfigDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private long experimentId;
    
    private long runId;
    
    private RunConfigImpl snapshot;
    
    private RunConfigImpl profiling;
    
    private RunConfigImpl schemaInference;
    
    private RunConfigImpl validation;
}

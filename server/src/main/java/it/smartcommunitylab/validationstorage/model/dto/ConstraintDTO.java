package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.TypedConstraint;

@Valid
public class ConstraintDTO {
    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    private String title;
    
    private String type;
    
    private String description;
    
    private int errorSeverity;
    
    private long[] resourceIds;
    
    private TypedConstraint constraint;
    
}

package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonUnwrapped;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;

@Valid
@JsonInclude(Include.NON_NULL)
public class ConstraintDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private Set<String> resourceIds;

    private String description;

    private Integer errorSeverity;

    @JsonUnwrapped
    private TypedConstraint constraint;
    
    public static ConstraintDTO from(Constraint source) {
        if (source == null)
            return null;
        
        ConstraintDTO dto = new ConstraintDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setResourceIds(source.getResourceIds());
        dto.setDescription(source.getDescription());
        dto.setConstraint(source.getConstraint());
        
        if (source.getErrorSeverity() != null)
            dto.setErrorSeverity(source.getErrorSeverity());
        else
            dto.setErrorSeverity(ValidationStorageConstants.DEFAULT_ERROR_SEVERITY);
        
        
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

    public String getExperimentId() {
        return experimentId;
    }

    public void setExperimentId(String experimentId) {
        this.experimentId = experimentId;
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

    public Set<String> getResourceIds() {
        return resourceIds;
    }

    public void setResourceIds(Set<String> resourceIds) {
        this.resourceIds = resourceIds;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getErrorSeverity() {
        return errorSeverity;
    }

    public void setErrorSeverity(Integer errorSeverity) {
        this.errorSeverity = errorSeverity;
    }

    public TypedConstraint getConstraint() {
        return constraint;
    }

    public void setConstraint(TypedConstraint constraint) {
        this.constraint = constraint;
    }

}

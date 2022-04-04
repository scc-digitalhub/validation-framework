package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
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
    @JsonProperty("project")
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("experiment")
    private String experimentName;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private Set<String> resources;

    private String description;

    private Integer weight;

    @JsonUnwrapped
    private TypedConstraint typedConstraint;
    
    public static ConstraintDTO from(Constraint source, String experimentName) {
        if (source == null)
            return null;
        
        ConstraintDTO dto = new ConstraintDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentName(experimentName);
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setResources(source.getResources());
        dto.setDescription(source.getDescription());
        dto.setTypedConstraint(source.getTypedConstraint());
        
        if (source.getWeight() != null)
            dto.setWeight(source.getWeight());
        else
            dto.setWeight(ValidationStorageConstants.DEFAULT_ERROR_SEVERITY);
        
        
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

    public String getExperimentName() {
        return experimentName;
    }

    public void setExperimentName(String experimentName) {
        this.experimentName = experimentName;
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

    public Set<String> getResources() {
        return resources;
    }

    public void setResources(Set<String> resources) {
        this.resources = resources;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getWeight() {
        return weight;
    }

    public void setWeight(Integer weight) {
        this.weight = weight;
    }

    public TypedConstraint getTypedConstraint() {
        return typedConstraint;
    }

    public void setTypedConstraint(TypedConstraint typedConstraint) {
        this.typedConstraint = typedConstraint;
    }

}

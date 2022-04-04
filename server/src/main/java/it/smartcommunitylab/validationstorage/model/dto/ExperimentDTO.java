package it.smartcommunitylab.validationstorage.model.dto;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunConfig;

/**
 * Request object: details an experiment.
 */
@Valid
@JsonInclude(Include.NON_NULL)
public class ExperimentDTO {
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private String description;

    @JsonProperty("config")
    private RunConfigDTO runConfig;

    private Set<String> tags;
    
    public static ExperimentDTO from(Experiment source) {
        if (source == null)
            return null;
        
        ExperimentDTO dto = new ExperimentDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setDescription(source.getDescription());
        dto.setRunConfig(RunConfigDTO.from(source.getRunConfig(), source.getName()));
        dto.setTags(new HashSet<String>(source.getTags()));
        
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public RunConfigDTO getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfigDTO runConfig) {
        this.runConfig = runConfig;
    }

    public Set<String> getTags() {
        return tags;
    }

    public void setTags(Set<String> tags) {
        this.tags = tags;
    }

}

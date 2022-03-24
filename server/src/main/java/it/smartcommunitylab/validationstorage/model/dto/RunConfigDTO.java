package it.smartcommunitylab.validationstorage.model.dto;

import java.util.Collections;
import java.util.List;
import java.util.UUID;

import javax.validation.Valid;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;

@Valid
@JsonInclude(Include.NON_NULL)
public class RunConfigDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    private List<RunConfigImpl> snapshot;

    private List<RunConfigImpl> profiling;

    @JsonProperty("inference")
    private List<RunConfigImpl> schemaInference;

    private List<RunConfigImpl> validation;

    public RunConfigDTO() {
        snapshot = Collections.<RunConfigImpl>emptyList();
        profiling = Collections.<RunConfigImpl>emptyList();
        schemaInference = Collections.<RunConfigImpl>emptyList();
        validation = Collections.<RunConfigImpl>emptyList();
    }
    
    public static RunConfigDTO from(RunConfig source) {
        if (source == null)
            return null;
        
        RunConfigDTO dto = new RunConfigDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        
        if (source.getSnapshot() != null)
            dto.setSnapshot(source.getSnapshot());
        
        if (source.getProfiling() != null)
            dto.setProfiling(source.getProfiling());
        
        if (source.getSchemaInference() != null)
            dto.setSchemaInference(source.getSchemaInference());
        
        if (source.getValidation() != null)
            dto.setValidation(source.getValidation());
        
        return dto;
    }
    
    public static RunConfig to(RunConfigDTO source) {
        if (source == null)
            return null;
        
        RunConfig document = new RunConfig();
        
        String id = source.getId();
        if (id == null)
            id = UUID.randomUUID().toString();
        
        document.setId(id);
        document.setProjectId(source.getProjectId());
        document.setExperimentId(source.getExperimentId());
        document.setSnapshot(source.getSnapshot());
        document.setProfiling(source.getProfiling());
        document.setSchemaInference(source.getSchemaInference());
        document.setValidation(source.getValidation());
        
        return document;
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

    public List<RunConfigImpl> getSnapshot() {
        return snapshot;
    }

    public void setSnapshot(List<RunConfigImpl> snapshot) {
        this.snapshot = snapshot;
    }

    public List<RunConfigImpl> getProfiling() {
        return profiling;
    }

    public void setProfiling(List<RunConfigImpl> profiling) {
        this.profiling = profiling;
    }

    public List<RunConfigImpl> getSchemaInference() {
        return schemaInference;
    }

    public void setSchemaInference(List<RunConfigImpl> schemaInference) {
        this.schemaInference = schemaInference;
    }

    public List<RunConfigImpl> getValidation() {
        return validation;
    }

    public void setValidation(List<RunConfigImpl> validation) {
        this.validation = validation;
    }

}

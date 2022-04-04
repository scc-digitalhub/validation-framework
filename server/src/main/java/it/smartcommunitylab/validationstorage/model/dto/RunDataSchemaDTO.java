package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.ReportMetadata;
import it.smartcommunitylab.validationstorage.model.RunDataSchema;
import it.smartcommunitylab.validationstorage.typed.TypedSchema;

/**
 * Request object: schema of the data.
 */
public class RunDataSchemaDTO {
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("experiment")
    private String experimentName;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("run")
    private String runId;

    private String resourceName;

    private String type;
    
    private ReportMetadata metadata;

    private TypedSchema schema;
    
    public static RunDataSchemaDTO from(RunDataSchema source, String experimentName) {
        if (source == null)
            return null;
        
        RunDataSchemaDTO dto = new RunDataSchemaDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentName(experimentName);
        dto.setRunId(source.getRunId());
        dto.setResourceName(source.getResourceName());
        dto.setType(source.getType());
        dto.setMetadata(source.getMetadata());
        dto.setSchema(source.getSchema());
        
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

    public String getRunId() {
        return runId;
    }

    public void setRunId(String runId) {
        this.runId = runId;
    }

    public String getResourceName() {
        return resourceName;
    }

    public void setResourceName(String resourceName) {
        this.resourceName = resourceName;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public ReportMetadata getMetadata() {
        return metadata;
    }

    public void setMetadata(ReportMetadata metadata) {
        this.metadata = metadata;
    }

    public TypedSchema getSchema() {
        return schema;
    }

    public void setSchema(TypedSchema schema) {
        this.schema = schema;
    }

}
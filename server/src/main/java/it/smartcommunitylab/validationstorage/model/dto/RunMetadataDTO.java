package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.ReportMetadata;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.RunStatus;

/**
 * Request object: lists metadata about a run.
 */
public class RunMetadataDTO {
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String runId;

    private LocalDate createdDate;

    private LocalDate startedDate;

    private LocalDate finishedDate;
    
    private RunStatus status;
    
    private ReportMetadata metadata;

    /**
     * May contain extra information.
     */
    @JsonIgnore
    private Map<String, Serializable> contents;

    public RunMetadataDTO() {
        contents = new HashMap<String, Serializable>();
    }

    public static RunMetadataDTO from(RunMetadata source) {
        if (source == null)
            return null;
        
        RunMetadataDTO dto = new RunMetadataDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setRunId(source.getRunId());
        dto.setCreatedDate(source.getCreatedDate());
        dto.setStartedDate(source.getStartedDate());
        dto.setFinishedDate(source.getFinishedDate());
        dto.setStatus(source.getStatus());
        dto.setMetadata(source.getMetadata());
        
        if (source.getContents() != null)
            dto.setContents(source.getContents());
        
        return dto;
    }
    
    @JsonAnyGetter
    public Map<String, Serializable> getContentMap() {
        return contents;
    }

    @JsonAnySetter
    public void addContent(String key, Serializable value) {
        contents.put(key, value);
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

    public String getRunId() {
        return runId;
    }

    public void setRunId(String runId) {
        this.runId = runId;
    }

    public LocalDate getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(LocalDate createdDate) {
        this.createdDate = createdDate;
    }

    public LocalDate getStartedDate() {
        return startedDate;
    }

    public void setStartedDate(LocalDate startedDate) {
        this.startedDate = startedDate;
    }

    public LocalDate getFinishedDate() {
        return finishedDate;
    }

    public void setFinishedDate(LocalDate finishedDate) {
        this.finishedDate = finishedDate;
    }
    
    public RunStatus getStatus() {
        return status;
    }

    public void setStatus(RunStatus status) {
        this.status = status;
    }

    public ReportMetadata getMetadata() {
        return metadata;
    }

    public void setMetadata(ReportMetadata metadata) {
        this.metadata = metadata;
    }

    public Map<String, Serializable> getContents() {
        return contents;
    }

    public void setContents(Map<String, Serializable> contents) {
        this.contents = contents;
    }

}
package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.RunStatus;

@Valid
public class RunDTO {
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String experimentId;

    @JsonProperty("config")
    private RunConfigDTO runConfig;

    @JsonProperty("package")
    private DataPackageDTO dataPackage;

    private List<ConstraintDTO> constraints;

    @JsonProperty("status")
    private RunStatus runStatus;

    private RunMetadataDTO runMetadata;

    private RunEnvironmentDTO runEnvironment;

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

    public RunConfigDTO getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfigDTO runConfig) {
        this.runConfig = runConfig;
    }

    public DataPackageDTO getDataPackage() {
        return dataPackage;
    }

    public void setDataPackage(DataPackageDTO dataPackage) {
        this.dataPackage = dataPackage;
    }

    public List<ConstraintDTO> getConstraints() {
        return constraints;
    }

    public void setConstraints(List<ConstraintDTO> constraints) {
        this.constraints = constraints;
    }

    public RunStatus getRunStatus() {
        return runStatus;
    }

    public void setRunStatus(RunStatus runStatus) {
        this.runStatus = runStatus;
    }

    public RunMetadataDTO getRunMetadata() {
        return runMetadata;
    }

    public void setRunMetadata(RunMetadataDTO runMetadata) {
        this.runMetadata = runMetadata;
    }

    public RunEnvironmentDTO getRunEnvironment() {
        return runEnvironment;
    }

    public void setRunEnvironment(RunEnvironmentDTO runEnvironment) {
        this.runEnvironment = runEnvironment;
    }

}

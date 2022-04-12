package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javax.validation.Valid;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunStatus;

@Valid
public class RunDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("experiment")
    private String experimentName;

    @JsonProperty("config")
    private RunConfigDTO runConfig;

    @JsonProperty("package")
    private DataPackageDTO dataPackage;

    private List<ConstraintDTO> constraints;

    @JsonProperty("status")
    private RunStatus runStatus;

    private RunMetadataDTO runMetadata;

    private RunEnvironmentDTO runEnvironment;
    
    public static RunDTO from(Run source, String experimentName) {
        if (source == null)
            return null;
        
        RunDTO dto = new RunDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentName(experimentName);
        dto.setRunConfig(RunConfigDTO.from(source.getRunConfig(), experimentName));
        
        // Package
        DataPackageDTO dataPackage = new DataPackageDTO();
        dataPackage.setName(source.getId());
        dataPackage.setTitle("Package for run " + source.getId());
        dataPackage.setType("run");
        
        // Package resources
        Map<String, DataResource> resources = source.getResources();
        if (resources != null) {
            List<DataResourceDTO> resourceDTOs = resources.values().stream().map(r -> DataResourceDTO.from(r)).collect(Collectors.toList());
            dataPackage.setResources(resourceDTOs);
        }
        dto.setDataPackage(dataPackage);
        
        // Constraints
        Map<String, Constraint> constraints = source.getConstraints();
        if (constraints != null) {
            List<ConstraintDTO> constraintDTOs = constraints.values().stream().map(c -> ConstraintDTO.from(c, experimentName)).collect(Collectors.toList());
            dto.setConstraints(constraintDTOs);
        }
        
        //dto.setConstraints(constraints);
        dto.setRunStatus(source.getRunStatus());
        dto.setRunMetadata(RunMetadataDTO.from(source.getRunMetadata(), experimentName));
        dto.setRunEnvironment(RunEnvironmentDTO.from(source.getRunEnvironment(), experimentName));
        
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

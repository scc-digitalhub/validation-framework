package it.smartcommunitylab.validationstorage.model.dto;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;

@Valid
@JsonInclude(Include.NON_NULL)
public class DataPackageDTO {
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

    private String type;

    private List<DataResourceDTO> resources;
    
    public static DataPackageDTO from(DataPackage source) {
        if (source == null)
            return null;
        
        DataPackageDTO dto = new DataPackageDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setType(source.getType());
        
        List<DataResourceDTO> resources = new ArrayList<DataResourceDTO>();
        if (source.getResources() != null) {
            for (DataResource i : source.getResources()) {
                resources.add(DataResourceDTO.from(i));
            }
        }
        dto.setResources(resources);
        
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

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public List<DataResourceDTO> getResources() {
        return resources;
    }

    public void setResources(List<DataResourceDTO> resources) {
        this.resources = resources;
    }

}

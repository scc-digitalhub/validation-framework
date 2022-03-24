package it.smartcommunitylab.validationstorage.model.dto;

import java.util.UUID;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonUnwrapped;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Dataset;
import it.smartcommunitylab.validationstorage.model.Schema;

@Valid
@JsonInclude(Include.NON_NULL)
public class DataResourceDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String packageName;

    // If null, will be the default store
    private String storeId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private String type;

    private Schema schema;

    @JsonUnwrapped
    private Dataset dataset;
    
    public static DataResourceDTO from(DataResource source) {
        if (source == null)
            return null;
        
        DataResourceDTO dto = new DataResourceDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setPackageName(source.getPackageName());
        dto.setStoreId(source.getStoreId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setType(source.getType());
        dto.setSchema(source.getSchema());
        dto.setDataset(source.getDataset());
        
        return dto;
    }
    
    public static DataResource to(DataResourceDTO source) {
        if (source == null)
            return null;
        
        DataResource document = new DataResource();
        
        String id = source.getId();
        if (id == null)
            id = UUID.randomUUID().toString();
        
        document.setId(id);
        document.setProjectId(source.getProjectId());
        document.setPackageName(source.getPackageName());
        document.setStoreId(source.getStoreId());
        document.setName(source.getName());
        document.setTitle(source.getTitle());
        document.setType(source.getType());
        document.setSchema(source.getSchema());
        document.setDataset(source.getDataset());
        
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

    public String getPackageName() {
        return packageName;
    }

    public void setPackageName(String packageName) {
        this.packageName = packageName;
    }

    public String getStoreId() {
        return storeId;
    }

    public void setStoreId(String storeId) {
        this.storeId = storeId;
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

    public Schema getSchema() {
        return schema;
    }

    public void setSchema(Schema schema) {
        this.schema = schema;
    }

    public Dataset getDataset() {
        return dataset;
    }

    public void setDataset(Dataset dataset) {
        this.dataset = dataset;
    }

}

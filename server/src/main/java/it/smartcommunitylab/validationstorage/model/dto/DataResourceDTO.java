package it.smartcommunitylab.validationstorage.model.dto;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonUnwrapped;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Dataset;
import it.smartcommunitylab.validationstorage.model.Schema;

@Valid
@JsonInclude(Include.NON_NULL)
public class DataResourceDTO {
    private String id;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @JsonProperty("project")
    private String projectId;

    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String packageName;

    // If null, will be the default store
    @JsonProperty("store")
    private String storeId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private String description;

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
        dto.setDescription(source.getDescription());
        dto.setType(source.getType());
        
        Schema sourceSchema = source.getSchema();
        if (sourceSchema.getType() == null)
            sourceSchema.setType(source.getType());
        dto.setSchema(sourceSchema);
        
        dto.setDataset(source.getDataset());
        
        return dto;
    }
    
    public static DataResource to(DataResourceDTO source, DataPackage dataPackage, String defaultStore) {
        if (source == null)
            return null;
        
        DataResource document = new DataResource();
        
        String id = source.getId();
        if (id == null)
            id = UUID.randomUUID().toString();
        
        document.setId(id);
        document.setProjectId(source.getProjectId());
        document.setPackageName(source.getPackageName());
        
        document.addPackage(dataPackage);
        
        if (source.getStoreId() != null)
            document.setStoreId(source.getStoreId());
        else
            document.setStoreId(defaultStore);
        
        document.setName(source.getName());
        document.setTitle(source.getTitle());
        document.setDescription(source.getDescription());
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
    
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
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

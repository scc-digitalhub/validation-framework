package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.AttributeOverride;
import javax.persistence.AttributeOverrides;
import javax.persistence.Column;
import javax.persistence.Embedded;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.ManyToMany;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Entity
@Table(name = "data_resource", uniqueConstraints = @UniqueConstraint(columnNames = { "package_name", "name" }))
public class DataResource {
    @Id
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;
    
    // Source package (user-defined)
    @Column(name = "package_name")
    private String packageName;
    
    // All packages that refer to this resource
    @ManyToMany(fetch = FetchType.LAZY)
    private List<DataPackage> packages;
    
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "store_id")
    private String storeId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;
    
    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    private String type;
    
    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name="schema", column=@Column(name="schema"))
    })
    private Schema schema;

    @Embedded
    @AttributeOverrides({
        @AttributeOverride(name="path", column=@Column(name="path"))
    })
    private Dataset dataset;

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

    public List<DataPackage> getPackages() {
        return packages;
    }

    public void setPackages(List<DataPackage> packages) {
        this.packages = packages;
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

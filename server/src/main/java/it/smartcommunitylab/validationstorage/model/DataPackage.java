package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.JoinColumn;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Entity
@Table(name = "packages", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "name" }))
public class DataPackage {

    @Id
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;
    
    private String type;

    @ManyToMany(mappedBy = "packages", fetch = FetchType.LAZY)
    private List<DataResource> resources;
    
    @Override
    public String toString() {
        return "DataPackage - project:" + projectId + ", name:" + name + ", title:" + title + ", type:" + type;
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

    public List<DataResource> getResources() {
        return resources;
    }

    public void setResources(List<DataResource> resources) {
        this.resources = resources;
    }
    
    public void addResource(DataResource dataResource) {
        if (dataResource == null)
            return;
        
        if (resources == null)
            resources = new ArrayList<DataResource>();
        
        resources.add(dataResource);
    }
    
}

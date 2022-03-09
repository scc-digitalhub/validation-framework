package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

@Entity
@Table(name = "experiments", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "name" }))
public class Experiment {
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
    
    private String description;
    
    @OneToOne
    @Column(name = "run_config")
    private RunConfig runConfig;
    
    @OneToOne
    @Column(name = "data_package")
    private DataPackage dataPackage;

    private List<String> tags;

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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public RunConfig getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfig runConfig) {
        this.runConfig = runConfig;
    }

    public DataPackage getDataPackage() {
        return dataPackage;
    }

    public void setDataPackage(DataPackage dataPackage) {
        this.dataPackage = dataPackage;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    
}

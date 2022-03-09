package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;
import java.util.Set;

import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.converter.StringSetConverter;
import it.smartcommunitylab.validationstorage.converter.TypedConstraintConverter;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;

@Entity
@Table(name = "constraints", uniqueConstraints = @UniqueConstraint(columnNames = { "experiment_id", "name" }))
public class Constraint implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = -7275307509940681567L;

    @Id
    private String id;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "project_id")
    private String projectId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    @Column(name = "experiment_id")
    private String experimentId;

    @NotBlank
    @Pattern(regexp = ValidationStorageConstants.NAME_PATTERN)
    private String name;

    @Pattern(regexp = ValidationStorageConstants.TITLE_PATTERN)
    private String title;

    @Lob
    @Column(name = "resource_ids")
    @Convert(converter = StringSetConverter.class)
    private Set<String> resourceIds;

    private String type;

    private String description;

    @Column(name = "error_severity")
    private Integer errorSeverity;

    @Lob
    @Convert(converter = TypedConstraintConverter.class)
    private TypedConstraint constraint;

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

    public Set<String> getResourceIds() {
        return resourceIds;
    }

    public void setResourceIds(Set<String> resourceIds) {
        this.resourceIds = resourceIds;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getErrorSeverity() {
        return errorSeverity;
    }

    public void setErrorSeverity(Integer errorSeverity) {
        this.errorSeverity = errorSeverity;
    }

    public TypedConstraint getConstraint() {
        return constraint;
    }

    public void setConstraint(TypedConstraint constraint) {
        this.constraint = constraint;
    }

    public static long getSerialversionuid() {
        return serialVersionUID;
    }

}

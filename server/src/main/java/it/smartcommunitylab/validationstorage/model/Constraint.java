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
@Table(name = "constraints", uniqueConstraints = @UniqueConstraint(columnNames = { "project_id", "experiment_id", "name" }))
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
    @Convert(converter = StringSetConverter.class)
    private Set<String> resources;

    private String type;

    private String description;

    private Integer weight;

    @Lob
    @Convert(converter = TypedConstraintConverter.class)
    @Column(name = "typed_constraint")
    private TypedConstraint typedConstraint;

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

    public Set<String> getResources() {
        return resources;
    }

    public void setResources(Set<String> resources) {
        this.resources = resources;
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

    public Integer getWeight() {
        return weight;
    }

    public void setWeight(Integer weight) {
        this.weight = weight;
    }

    public TypedConstraint getTypedConstraint() {
        return typedConstraint;
    }

    public void setTypedConstraint(TypedConstraint typedConstraint) {
        this.typedConstraint = typedConstraint;
    }

    public static long getSerialversionuid() {
        return serialVersionUID;
    }

}

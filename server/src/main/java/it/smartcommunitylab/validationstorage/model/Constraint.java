package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import com.fasterxml.jackson.annotation.JsonUnwrapped;

@Entity
public class Constraint {
    @Id
    @GeneratedValue
    private long id;
    
    private Project project;
    
    private Experiment experiment;
    
    private Run run;
    
    private List<DataResource> resources;
    
    private String name;
    
    private String title;
    
    private String type;
    
    private String description;
    
    @JsonUnwrapped
    private int errorSeverity;
    
    private TypedConstraint constraint;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public Experiment getExperiment() {
        return experiment;
    }

    public void setExperiment(Experiment experiment) {
        this.experiment = experiment;
    }

    public Run getRun() {
        return run;
    }

    public void setRun(Run run) {
        this.run = run;
    }

    public List<DataResource> getResources() {
        return resources;
    }

    public void setResources(List<DataResource> resources) {
        this.resources = resources;
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getErrorSeverity() {
        return errorSeverity;
    }

    public void setErrorSeverity(int errorSeverity) {
        this.errorSeverity = errorSeverity;
    }

    public TypedConstraint getConstraint() {
        return constraint;
    }

    public void setConstraint(TypedConstraint constraint) {
        this.constraint = constraint;
    }
    
}

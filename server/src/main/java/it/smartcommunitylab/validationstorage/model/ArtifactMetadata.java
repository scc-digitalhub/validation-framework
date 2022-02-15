package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Metadata about artifact files related to a run.
 */
@Entity
public class ArtifactMetadata {
    @Id
    @GeneratedValue
    private long id;

    private Project project;

    private Experiment experiment;
    
    private Run run;

    /**
     * File name.
     */
    private String name;

    /**
     * File location.
     */
    private String uri;
    
    /**
     * Creator of this document.
     */
    private String author;

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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        this.uri = uri;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
    
    
    
}
package it.smartcommunitylab.validationstorage.model;

import java.util.Map;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;

/**
 * Schema of the data.
 */
@Entity
public class ShortSchema {
    @Id
    @GeneratedValue
    private long id;

    private Project project;

    private Experiment experiment;
    
    private Run run;

    /**
     * Creator of this document.
     */
    private String author;

    /**
     * May contain extra information.
     */
    private Map<String, ?> contents;

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

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public Map<String, ?> getContents() {
        return contents;
    }

    public void setContents(Map<String, ?> contents) {
        this.contents = contents;
    }
    
}
package it.smartcommunitylab.validationstorage.model;

import javax.validation.Valid;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Details a project.
 */
@Valid
@Document
public class Project {
    /**
     * Unique ID.
     */
    @Id
    private String id;

    /**
     * Name of the project.
     */
    private String name;

    /**
     * Creator of this document.
     */
    private String author;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
    
}

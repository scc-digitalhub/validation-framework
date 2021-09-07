package it.smartcommunitylab.validationstorage.model;

import java.util.Date;
import java.util.Map;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;
import lombok.NonNull;

/**
 * Lists metadata about a run.
 */
@Data
@Document
public class RunMetadata {
    /**
     * Unique ID of this document.
     */
    @Id
    private String id;

    /**
     * ID of the project this document belongs to.
     */
    @NonNull
    private String projectId;

    /**
     * ID of the experiment this document belongs to.
     */
    @NonNull
    private String experimentId;

    /**
     * ID of the run. Only unique within the combination of experiment and project.
     */
    @NonNull
    private String runId;

    /**
     * Name of the experiment this document belongs to.
     */
    private String experimentName;

    /**
     * Timestamp of the run's creation, taken from 'contents'. If not specified in 'contents', will be the time of creation of this document.
     */
    private Date created;

    /**
     * Creator of this document.
     */
    private String author;

    /**
     * May contain extra information.
     */
    private Map<String, ?> contents;
}
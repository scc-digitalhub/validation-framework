package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;
import lombok.NonNull;

/**
 * Metadata about artifact files related to a run.
 */
@Data
@Document
public class ArtifactMetadata {
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
     * ID of the run this document belongs to.
     */
    @NonNull
    private String runId;

    /**
     * File name.
     */
    @NonNull
    private String name;

    /**
     * File location.
     */
    @NonNull
    private String uri;

    /**
     * Name of the experiment this document belongs to.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;
}
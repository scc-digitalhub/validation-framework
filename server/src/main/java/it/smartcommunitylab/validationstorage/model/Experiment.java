package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;
import lombok.NonNull;

/**
 * Details an experiment.
 */
@Data
@Document
public class Experiment {
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
     * ID of the experiment. Only unique within the project it belongs to.
     */
    @NonNull
    private String experimentId;

    /**
     * Name of the experiment.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;
}

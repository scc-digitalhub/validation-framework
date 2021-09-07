package it.smartcommunitylab.validationstorage.model;

import java.util.Map;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;
import lombok.NonNull;

/**
 * Short report on the validation's result.
 */
@Data
@Document
public class RunEnvironment {
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
     * Name of the experiment this document belongs to.
     */
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;

    /**
     * May contain extra information.
     */
    private Map<String, ?> contents;
}
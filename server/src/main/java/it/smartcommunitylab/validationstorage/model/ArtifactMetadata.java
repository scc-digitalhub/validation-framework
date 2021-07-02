package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonProperty;

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
    @JsonProperty("project_id")
    @Field("project_id")
    private String projectId;

    /**
     * ID of the experiment this document belongs to.
     */
    @NonNull
    @JsonProperty("experiment_id")
    @Field("experiment_id")
    private String experimentId;

    /**
     * ID of the run this document belongs to.
     */
    @NonNull
    @JsonProperty("run_id")
    @Field("run_id")
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
    @JsonProperty("experiment_name")
    @Field("experiment_name")
    private String experimentName;

    /**
     * Creator of this document.
     */
    private String author;
}
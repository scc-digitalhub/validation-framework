package it.smartcommunitylab.validationstorage.model;

import java.util.Map;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;
import lombok.NonNull;

/**
 * Profile for the data.
 */
@Data
@Document
public class DataProfile {
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
     * Name of the experiment this document belongs to.
     */
    @JsonProperty("experiment_name")
    @Field("experiment_name")
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
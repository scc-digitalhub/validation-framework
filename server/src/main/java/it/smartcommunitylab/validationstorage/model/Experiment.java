package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonProperty;

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
	@JsonProperty("project_id")
	@Field("project_id")
	private String projectId;
	
	/**
	 * ID of the experiment. Only unique within the project it belongs to.
	 */
	@NonNull
	@JsonProperty("experiment_id")
	@Field("experiment_id")
	private String experimentId;
	
	/**
	 * Name of the experiment.
	 */
	@JsonProperty("experiment_name")
	@Field("experiment_name")
	private String experimentName;
}

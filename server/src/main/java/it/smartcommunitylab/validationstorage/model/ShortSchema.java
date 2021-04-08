package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;
import lombok.NonNull;

@Data
@Document
public class ShortSchema {
	@Id
	private String id;
	
	@NonNull
	@JsonProperty("project_id")
	@Field("project_id")
	private String projectId;
	
	@NonNull
	@JsonProperty("experiment_id")
	@Field("experiment_id")
	private String experimentId;
	
	@NonNull
	@JsonProperty("run_id")
	@Field("run_id")
	private String runId;
	
	@JsonProperty("experiment_name")
	@Field("experiment_name")
	private String experimentName;
	
	private Object contents;
}
package it.smartcommunitylab.validationstorage.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class RunMetadataDTO {
	
	@JsonProperty("experiment_id")
	private String experimentId;
	
	@JsonProperty("experiment_name")
	private String experimentName;
	
	@JsonProperty("run_id")
	private String runId;
	
	private Object contents;
}
package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonProperty;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import lombok.Data;

/**
 * Request object: short report on the validation's result.
 */
@Data
@Valid
public class RunEnvironmentDTO {
	/**
	 * ID of the experiment this document belongs to.
	 */
	@JsonProperty("experiment_id")
	@NotBlank
	@Pattern(regexp=ValidationStorageUtils.ID_PATTERN)
	private String experimentId;
	
	/**
	 * Name of the experiment this document belongs to.
	 */
	@JsonProperty("experiment_name")
	@Pattern(regexp=ValidationStorageUtils.NAME_PATTERN)
	private String experimentName;
	
	/**
	 * ID of the run this document belongs to.
	 */
	@JsonProperty("run_id")
	@NotBlank
	@Pattern(regexp=ValidationStorageUtils.ID_PATTERN)
	private String runId;
	
	/**
	 * May contain extra information.
	 */
	private Map<String, Serializable> contents;
}
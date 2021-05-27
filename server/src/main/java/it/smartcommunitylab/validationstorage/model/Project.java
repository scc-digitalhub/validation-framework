package it.smartcommunitylab.validationstorage.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;

/**
 * Details a project.
 */
@Data
@Document
public class Project {
	/**
	 * Unique ID.
	 */
	@Id
	private String id;
	
	/**
	 * Name of the project.
	 */
	private String name;
}

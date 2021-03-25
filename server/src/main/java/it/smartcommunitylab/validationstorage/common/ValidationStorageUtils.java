package it.smartcommunitylab.validationstorage.common;

import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public class ValidationStorageUtils {
	public static final String ARTIFACT_METADATA = "artifact-metadata";
	public static final String DATA_RESOURCE = "data-resource";
	public static final String RUN_METADATA = "run-metadata";
	public static final String SHORT_REPORT = "report-short";
	
	public enum OperationType {
		CREATE, READ, UPDATE, DELETE
	}
	
	public static void checkUserHasPermissions(OperationType opType, String projectId) {
		// TODO
		boolean allowed = true;
		
		if (!allowed)
			throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "User is not allowed to perform this operation.");
	}
	
	public static void checkProjectIdMatch(String id, String documentProjectId, String projectId) {
		if (!documentProjectId.equals(projectId))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document with ID " + id + " has project ID " + documentProjectId + ", which does not match the specified project ID " + projectId + ".");
	}
	
}
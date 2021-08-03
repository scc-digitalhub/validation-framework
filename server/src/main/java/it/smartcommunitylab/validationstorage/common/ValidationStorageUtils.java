package it.smartcommunitylab.validationstorage.common;

import org.springframework.security.core.Authentication;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;

import java.text.Normalizer;

/**
 * Various constants and utility methods used throughout the application are grouped here.
 */
public class ValidationStorageUtils {
    // Constants used to determine the path of certain end-points
    public static final String ARTIFACT_METADATA = "artifact-metadata";
    public static final String DATA_RESOURCE = "data-resource";
    public static final String DATA_PROFILE = "data-profile";
    public static final String EXPERIMENT = "experiment";
    public static final String RUN_ENVIRONMENT = "run-environment";
    public static final String RUN_METADATA = "run-metadata";
    public static final String SHORT_REPORT = "short-report";
    public static final String SHORT_SCHEMA = "short-schema";

    // RunMetadata documents act as representatives for the run they refer to. This is especially true for the UI,
    // where all data related to a run is nested within the RunMetadata document. To make this nesting more explicit,
    // UI end-points will use this constant for the portion of the path that identifies a run.
    public static final String RUN = "run";

    // Date format and contents field for dates in RunMetadata documents
    public static final String DATE_FORMAT = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX";
    public static final String FIELD_RUN_METADATA_TS = "created";

    // Conditions for PreAuthorize and similar annotations
    public static final String PREAUTH_PROJECTID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #projectId)";
    public static final String PREAUTH_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #id)";
    public static final String PREAUTH_REQUEST_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #request.getId())";
    public static final String POSTFILTER_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + filterObject.getId())";

    // Patterns to check validity of ID and name fields
    public static final String ID_PATTERN = "^[a-zA-Z0-9_-]+$";
    public static final String NAME_PATTERN = "^[a-zA-Z0-9 _-]+$";

    /**
     * Checks if the indicated project ID matches the document's.
     * 
     * @param id                ID of the document, used to print a more complete message if needed.
     * @param documentProjectId The document's project ID.
     * @param projectId         Project ID indicated by the API call.
     */
    public static void checkProjectIdMatch(String id, String documentProjectId, String projectId) {
        if (!documentProjectId.equals(projectId))
            throw new IllegalArgumentException("Document with ID " + id + " has project ID " + documentProjectId + ", which does not match the specified project ID " + projectId + ".");
    }

    /**
     * Converts string to lower case, removes accents and other diacritics.
     * 
     * @param input String to normalize.
     * @return Result of input normalization.
     */
    public static String normalizeString(String input) {
        return Normalizer.normalize(input.toLowerCase(), Normalizer.Form.NFKD).replaceAll("\\p{InCombiningDiacriticalMarks}+", "");
    }

    /**
     * Checks if a project exists.
     * 
     * @param id ID of the project.
     */
    public static void checkProjectExists(ProjectRepository repository, String id) {
        if (!repository.findById(id).isPresent())
            throw new DocumentNotFoundException("Project with ID " + id + " does not exist.");
    }

    /**
     * Creates an Experiment document.
     * 
     * @param projectId      ID of the project the experiment belongs to.
     * @param experimentId   ID of the experiment.
     * @param experimentName Name of the experiment.
     */
    public static void createExperiment(ExperimentRepository repository, String projectId, String experimentId, String experimentName) {
        if (repository.findByProjectIdAndExperimentId(projectId, experimentId).size() == 0) {
            Experiment experimentToSave = new Experiment(projectId, experimentId);
            if (!ObjectUtils.isEmpty(experimentName))
                experimentToSave.setExperimentName(experimentName);
            repository.save(experimentToSave);
        }
    }

    public static String getAuthorName(Authentication authentication) {
        if (authentication != null)
            return authentication.getName();
        return null;
    }
}
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
    /**
     * Checks if the indicated project ID matches the document's.
     * 
     * @param id                ID of the document, used to print a more complete message if needed.
     * @param documentProjectId The document's project ID.
     * @param projectId         Project ID indicated by the API call.
     */
    public static void checkProjectIdMatch(String id, String documentProjectId, String projectId) {
        if (!documentProjectId.equals(projectId))
            throw new IllegalArgumentException("Specified project ID does not match the value contained in the document.");
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
    public static void createExperiment(ExperimentRepository repository, String projectId, String experimentId, String experimentName, String author) {
        if (repository.findByProjectIdAndExperimentId(projectId, experimentId).size() == 0) {
            Experiment experimentToSave = new Experiment(projectId, experimentId);
            if (!ObjectUtils.isEmpty(experimentName))
                experimentToSave.setExperimentName(experimentName);
            if (!ObjectUtils.isEmpty(author))
                experimentToSave.setAuthor(author);
            repository.save(experimentToSave);
        }
    }

    /**
     * Get author name from authentication.
     * 
     * @param authentication Authentication.
     * @return Author name.
     */
    public static String getAuthorName(Authentication authentication) {
        if (authentication != null)
            return authentication.getName();
        return null;
    }
}
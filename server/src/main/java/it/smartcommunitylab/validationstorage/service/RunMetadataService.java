package it.smartcommunitylab.validationstorage.service;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.DataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import it.smartcommunitylab.validationstorage.repository.ShortSchemaRepository;

@Service
public class RunMetadataService {
    @Autowired
    private RunMetadataRepository documentRepository;

    @Autowired
    private ProjectRepository projectRepository;
    @Autowired
    private ExperimentRepository experimentRepository;
    @Autowired
    private ArtifactMetadataRepository artifactMetadataRepository;
    @Autowired
    private DataProfileRepository dataProfileRepository;
    @Autowired
    private DataResourceRepository dataResourceRepository;
    @Autowired
    private RunEnvironmentRepository runEnvironmentRepository;
    @Autowired
    private ShortReportRepository shortReportRepository;
    @Autowired
    private ShortSchemaRepository shortSchemaRepository;

    /**
     * Given an ID, returns the corresponding document, or null if it can't be found.
     * 
     * @param id ID of the document to retrieve.
     * @return The document if found, null otherwise.
     */
    private RunMetadata getDocument(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunMetadata> o = documentRepository.findById(id);
        if (o.isPresent()) {
            RunMetadata document = o.get();
            return document;
        }
        return null;
    }

    /**
     * Filters a list by a term.
     * 
     * @param items  List to filter.
     * @param search A term to filter results by.
     * @return A new list, with only the results that found a match.
     */
    private List<RunMetadata> filterBySearch(List<RunMetadata> items, String search) {
        if (ObjectUtils.isEmpty(search))
            return items;

        String normalized = ValidationStorageUtils.normalizeString(search);

        List<RunMetadata> results = new ArrayList<RunMetadata>();
        for (RunMetadata item : items) {
            if (item.getExperimentName().toLowerCase().contains(normalized))
                results.add(item);
        }

        return results;
    }

    // Create
    /**
     * Create a RunMetadata document. If overwriteParam is specified and equal to true, it will delete the
     * previous (if present) RunMetadata document that matches the same projectId, experimentId and runId.
     * All documents of other types under it will also be deleted.
     * 
     * @param projectId      ID of the project the document belongs to.
     * @param request        Request object describing the document.
     * @param overwriteParam If 'true', completely overwrites a previous RunMetadata identified by (projectId, experimentId, runId).
     * @return The created document.
     */
    public RunMetadata createDocument(String projectId, RunMetadataDTO request, Optional<String> overwriteParam, String author) {
        if (ObjectUtils.isEmpty(projectId))
            throw new IllegalArgumentException("Project ID is missing or blank.");
        ValidationStorageUtils.checkProjectExists(projectRepository, projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();

        if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)))
            throw new IllegalArgumentException("Fields 'experimentId', 'runId' are required and cannot be blank.");

        // The overwrite operation is only performed if 'overwriteParam' is present and equal to 'true'.
        Boolean overwrite = false;
        if (overwriteParam.isPresent() && !(ObjectUtils.isEmpty(overwriteParam.get())) && (overwriteParam.get().equals("true")))
            overwrite = true;

        if ((!overwrite) && (!(documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId).isEmpty())))
            throw new DocumentAlreadyExistsException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") already exists.");
        else if (overwrite) {
            // Deletes all documents under the RunMetadata document identified by (projectId, experimentId, runId).
            documentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);

            artifactMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
            dataResourceRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
            dataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
            runEnvironmentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
            shortReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
            shortSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        }

        RunMetadata documentToSave = new RunMetadata(projectId, experimentId, runId);

        // If the 'contents' field contains a 'created' field, it will also be stored in a dedicated field.
        // Otherwise, it will take the current timestamp.
        Date ts;
        try {
            ts = new SimpleDateFormat(ValidationStorageConstants.DATE_FORMAT).parse(request.getContents().get(ValidationStorageConstants.FIELD_RUN_METADATA_TS).toString());
        } catch (NullPointerException | ParseException e) {
            ts = new Date(System.currentTimeMillis());
        }
        documentToSave.setCreated(ts);

        documentToSave.setExperimentName(request.getExperimentName());
        documentToSave.setAuthor(author);
        documentToSave.setContents(request.getContents());

        // Create experiment document automatically.
        ValidationStorageUtils.createExperiment(experimentRepository, projectId, experimentId, request.getExperimentName(), author);

        return documentRepository.save(documentToSave);
    }

    // Read
    public List<RunMetadata> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        List<RunMetadata> repositoryResults;

        if (experimentId.isPresent() && runId.isPresent())
            repositoryResults = documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId.get(), runId.get());
        else if (experimentId.isPresent())
            repositoryResults = documentRepository.findByProjectIdAndExperimentId(projectId, experimentId.get());
        else if (runId.isPresent())
            repositoryResults = documentRepository.findByProjectIdAndRunId(projectId, runId.get());
        else
            repositoryResults = documentRepository.findByProjectId(projectId);

        if (search.isPresent())
            repositoryResults = filterBySearch(repositoryResults, search.get());

        return repositoryResults;
    }

    public RunMetadata findDocumentById(String projectId, String id) {
        RunMetadata document = getDocument(id);
        if (document != null) {
            ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);

            return document;
        }
        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
    }

    // Update
    public RunMetadata updateDocument(String projectId, String id, RunMetadataDTO request) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID is missing or blank.");

        RunMetadata document = getDocument(id);
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");

        ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();
        if ((experimentId != null && !(experimentId.equals(document.getExperimentId()))) || (runId != null && (!runId.equals(document.getRunId()))))
            throw new IllegalArgumentException("A value was specified for experimentId and/or runId, but they do not match the values in the document with ID " + id + ". Are you sure you are trying to update the correct document?");

        document.setExperimentName(request.getExperimentName());
        document.setContents(request.getContents());

        return documentRepository.save(document);
    }

    // Delete
    public void deleteDocumentById(String projectId, String id) {
        RunMetadata document = getDocument(id);
        if (document != null) {
            ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);

            documentRepository.deleteById(id);
            return;
        }
        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
    }

    // Delete
    public void deleteDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId) {
        if (experimentId.isPresent() && runId.isPresent())
            documentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId.get(), runId.get());
        else if (experimentId.isPresent())
            documentRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
        else if (runId.isPresent())
            documentRepository.deleteByProjectIdAndRunId(projectId, runId.get());
        else
            documentRepository.deleteByProjectId(projectId);
    }

}
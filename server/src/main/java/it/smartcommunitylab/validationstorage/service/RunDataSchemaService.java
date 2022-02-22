package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.IdMismatchException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.RunDataSchema;
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

@Service
public class RunDataSchemaService {
    @Autowired
    private RunDataSchemaRepository documentRepository;

    @Autowired
    private ProjectService projectService;
    @Autowired
    private ExperimentService experimentService;

    /**
     * Given an ID, returns the corresponding document, or null if it can't be found.
     * 
     * @param id ID of the document to retrieve.
     * @return The document if found, null otherwise.
     */
    private RunDataSchema getDocument(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunDataSchema> o = documentRepository.findById(id);
        if (o.isPresent()) {
            RunDataSchema document = o.get();
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
    private List<RunDataSchema> filterBySearch(List<RunDataSchema> items, String search) {
        if (ObjectUtils.isEmpty(search))
            return items;

        String normalized = ValidationStorageUtils.normalizeString(search);

        List<RunDataSchema> results = new ArrayList<RunDataSchema>();
        for (RunDataSchema item : items) {
            if (item.getExperimentName().toLowerCase().contains(normalized))
                results.add(item);
        }

        return results;
    }

    // Create
    public RunDataSchema createDocument(String projectId, RunDataSchemaDTO request, String author) {
        if (ObjectUtils.isEmpty(projectId))
            throw new IllegalArgumentException("Project ID is missing or blank.");
        projectService.findDocumentById(projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();

        if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)))
            throw new IllegalArgumentException("Fields 'experimentId', 'runId' are required and cannot be blank.");

        if (!(documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId).isEmpty()))
            throw new DocumentAlreadyExistsException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + ") already exists.");

        RunDataSchema documentToSave = new RunDataSchema(projectId, experimentId, runId);

        documentToSave.setExperimentName(request.getExperimentName());
        documentToSave.setAuthor(author);
        documentToSave.setContents(request.getContents());

        // Create experiment document automatically.
        experimentService.createExperimentIfMissing(projectId, experimentId, request.getExperimentName(), author);

        return documentRepository.save(documentToSave);
    }

    // Read
    public List<RunDataSchema> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        List<RunDataSchema> repositoryResults;

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

    // Read
    public RunDataSchema findDocumentById(String projectId, String id) {
        RunDataSchema document = getDocument(id);
        if (document != null) {
            if (!document.getProjectId().equals(projectId))
                throw new IdMismatchException();

            return document;
        }
        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
    }

    // Update
    public RunDataSchema updateDocument(String projectId, String id, RunDataSchemaDTO request) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID is missing or blank.");

        RunDataSchema document = getDocument(id);
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");

        if (!document.getProjectId().equals(projectId))
            throw new IdMismatchException();

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
        RunDataSchema document = getDocument(id);
        if (document != null) {
            if (!document.getProjectId().equals(projectId))
                throw new IdMismatchException();

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
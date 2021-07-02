package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.model.dto.ShortReportDTO;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ShortReportService {
    private final ShortReportRepository documentRepository;

    private final ProjectRepository projectRepository;
    private final ExperimentRepository experimentRepository;

    /**
     * Given an ID, returns the corresponding document, or null if it can't be found.
     * 
     * @param id ID of the document to retrieve.
     * @return The document if found, null otherwise.
     */
    private ShortReport getDocument(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<ShortReport> o = documentRepository.findById(id);
        if (o.isPresent()) {
            ShortReport document = o.get();
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
    private List<ShortReport> filterBySearch(List<ShortReport> items, String search) {
        if (ObjectUtils.isEmpty(search))
            return items;

        String normalized = ValidationStorageUtils.normalizeString(search);

        List<ShortReport> results = new ArrayList<ShortReport>();
        for (ShortReport item : items) {
            if (item.getExperimentName().toLowerCase().contains(normalized))
                results.add(item);
        }

        return results;
    }

    // Create
    public ShortReport createDocument(String projectId, ShortReportDTO request, String author) {
        if (ObjectUtils.isEmpty(projectId))
            throw new IllegalArgumentException("Project ID is missing or blank.");
        ValidationStorageUtils.checkProjectExists(projectRepository, projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();

        if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)))
            throw new IllegalArgumentException("Fields 'experiment_id', 'run_id' are required and cannot be blank.");

        if (!(documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId).isEmpty()))
            throw new DocumentAlreadyExistsException("Document (project_id=" + projectId + ", experiment_id=" + experimentId + ", run_id=" + runId + ") already exists.");

        ShortReport documentToSave = new ShortReport(projectId, experimentId, runId);

        documentToSave.setExperimentName(request.getExperimentName());
        documentToSave.setAuthor(author);
        documentToSave.setContents(request.getContents());

        // Create experiment document automatically.
        ValidationStorageUtils.createExperiment(experimentRepository, projectId, experimentId, request.getExperimentName());

        return documentRepository.save(documentToSave);
    }

    // Read
    public List<ShortReport> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        List<ShortReport> repositoryResults;

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
    public ShortReport findDocumentById(String projectId, String id) {
        ShortReport document = getDocument(id);
        if (document != null) {
            ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);

            return document;
        }
        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
    }

    // Update
    public ShortReport updateDocument(String projectId, String id, ShortReportDTO request) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID is missing or blank.");

        ShortReport document = getDocument(id);
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");

        ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();
        if ((experimentId != null && !(experimentId.equals(document.getExperimentId()))) || (runId != null && (!runId.equals(document.getRunId()))))
            throw new IllegalArgumentException("A value was specified for experiment_id and/or run_id, but they do not match the values in the document with ID " + id + ". Are you sure you are trying to update the correct document?");

        document.setExperimentName(request.getExperimentName());
        document.setContents(request.getContents());

        return documentRepository.save(document);
    }

    // Delete
    public void deleteDocumentById(String projectId, String id) {
        ShortReport document = getDocument(id);
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
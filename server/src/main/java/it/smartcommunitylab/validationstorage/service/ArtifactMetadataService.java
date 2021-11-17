package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.IdMismatchException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;

@Service
public class ArtifactMetadataService {
    @Autowired
    private ArtifactMetadataRepository documentRepository;
    
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
    private ArtifactMetadata getDocument(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<ArtifactMetadata> o = documentRepository.findById(id);
        if (o.isPresent()) {
            ArtifactMetadata document = o.get();
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
    private List<ArtifactMetadata> filterBySearch(List<ArtifactMetadata> items, String search) {
        if (ObjectUtils.isEmpty(search))
            return items;

        String normalized = ValidationStorageUtils.normalizeString(search);

        List<ArtifactMetadata> results = new ArrayList<ArtifactMetadata>();
        for (ArtifactMetadata item : items) {
            if (item.getExperimentName().toLowerCase().contains(normalized) || (item.getName().toLowerCase().contains(normalized)))
                results.add(item);
        }

        return results;
    }

    // Create
    public ArtifactMetadata createDocument(String projectId, ArtifactMetadataDTO request, String author) {
        if (ObjectUtils.isEmpty(projectId))
            throw new IllegalArgumentException("Project ID is missing or blank.");

        projectService.findDocumentById(projectId);

        String experimentId = request.getExperimentId();
        String runId = request.getRunId();
        String name = request.getName();
        String uri = request.getUri();

        if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)) || (ObjectUtils.isEmpty(name)) || (ObjectUtils.isEmpty(uri)))
            throw new IllegalArgumentException("Fields 'experimentId', 'runId', 'name', 'uri' are required and cannot be blank.");

        ArtifactMetadata documentToSave = new ArtifactMetadata(projectId, experimentId, runId, name, uri);

        documentToSave.setExperimentName(request.getExperimentName());
        documentToSave.setAuthor(author);

        // Create experiment document automatically.
        experimentService.createExperimentIfMissing(projectId, experimentId, request.getExperimentName(), author);

        return documentRepository.save(documentToSave);
    }

    // Read
    public List<ArtifactMetadata> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        List<ArtifactMetadata> repositoryResults;

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
    public ArtifactMetadata findDocumentById(String projectId, String id) {
        ArtifactMetadata document = getDocument(id);
        if (document != null) {
            if (!document.getProjectId().equals(projectId))
                throw new IdMismatchException();

            return document;
        }
        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
    }

    // Update
    public ArtifactMetadata updateDocument(String projectId, String id, ArtifactMetadataDTO request) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID is missing or blank.");

        ArtifactMetadata document = getDocument(id);
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");

        if (!document.getProjectId().equals(projectId))
            throw new IdMismatchException();

        document.setExperimentId(request.getExperimentId());
        document.setExperimentName(request.getExperimentName());
        document.setRunId(request.getRunId());
        document.setName(request.getName());
        document.setUri(request.getUri());

        return documentRepository.save(document);
    }

    // Delete
    public void deleteDocumentById(String projectId, String id) {
        ArtifactMetadata document = getDocument(id);
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
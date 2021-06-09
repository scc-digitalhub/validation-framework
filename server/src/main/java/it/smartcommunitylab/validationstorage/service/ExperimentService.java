package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.DataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import it.smartcommunitylab.validationstorage.repository.ShortSchemaRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ExperimentService {
	private final ExperimentRepository documentRepository;
	
	private final ArtifactMetadataRepository artifactMetadataRepository;
	private final DataProfileRepository dataProfileRepository;
	private final DataResourceRepository dataResourceRepository;
	private final ProjectRepository projectRepository;
	private final RunMetadataRepository runMetadataRepository;
	private final ShortReportRepository shortReportRepository;
	private final ShortSchemaRepository shortSchemaRepository;
	
	/**
	 * Given an ID, returns the corresponding document, or null if it can't be found.
	 * @param id ID of the document to retrieve.
	 * @return The document if found, null otherwise.
	 */
	private Experiment getDocument(String id) {
		if (ObjectUtils.isEmpty(id))
			return null;
		
		Optional<Experiment> o = documentRepository.findById(id);
		if (o.isPresent()) {
			Experiment document = o.get();
			return document;
		}
		return null;
	}
	
	/**
	 * Filters a list by a term.
	 * @param items List to filter.
	 * @param search A term to filter results by.
	 * @return A new list, with only the results that found a match.
	 */
	private List<Experiment> filterBySearch(List<Experiment> items, String search) {
		if (ObjectUtils.isEmpty(search))
			return items;
		
		String normalized = ValidationStorageUtils.normalizeString(search);
		
		List<Experiment> results = new ArrayList<Experiment>();
		for (Experiment item : items) {
			if (item.getExperimentName().toLowerCase().contains(normalized))
				results.add(item);
		}
		
		return results;
	}
	
	// Create
	public Experiment createDocument(String projectId, ExperimentDTO request, String author) {
		if (ObjectUtils.isEmpty(projectId))
			throw new IllegalArgumentException("Project ID is missing or blank.");
		ValidationStorageUtils.checkProjectExists(projectRepository, projectId);
		
		String experimentId = request.getExperimentId();
		
		if (ObjectUtils.isEmpty(experimentId))
			throw new IllegalArgumentException("Field 'experiment_id' is required and cannot be blank.");
		
		if (!(documentRepository.findByProjectIdAndExperimentId(projectId, experimentId).isEmpty()))
			throw new DocumentAlreadyExistsException("Document (project_id=" + projectId + ", experiment_id=" + experimentId + ") already exists.");
		
		Experiment documentToSave = new Experiment(projectId, experimentId);
		
		documentToSave.setExperimentName(request.getExperimentName());
		documentToSave.setAuthor(author);
		
		return documentRepository.save(documentToSave);
	}
	
	// Read
	public List<Experiment> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> search) {
		List<Experiment> repositoryResults;
		
		if (experimentId.isPresent())
			repositoryResults = documentRepository.findByProjectIdAndExperimentId(projectId, experimentId.get());
		else
			repositoryResults = documentRepository.findByProjectId(projectId);
		
		if (search.isPresent())
			repositoryResults = filterBySearch(repositoryResults, search.get());
		
		return repositoryResults;
	}
	
	// Read
	public Experiment findDocumentById(String projectId, String id) {
		Experiment document = getDocument(id);
		if (document != null) {
			ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
			
			return document;
		}
		throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
	}
	
	// Update
	public Experiment updateDocument(String projectId, String id, ExperimentDTO request) {
		if (ObjectUtils.isEmpty(id))
			throw new IllegalArgumentException("Document ID is missing or blank.");
		
		Experiment document = getDocument(id);
		if (document == null)
			throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
		
		ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
		
		String experimentId = request.getExperimentId();
		if (experimentId != null && !(experimentId.equals(document.getExperimentId())))
			throw new IllegalArgumentException("A value was specified for experiment_id, but does not match the value in the document with ID " + id + ". Are you sure you are trying to update the correct document?");
		
		document.setExperimentName(request.getExperimentName());
		
		return documentRepository.save(document);
	}
	
	// Delete
	public void deleteDocumentById(String projectId, String id) {
		Experiment document = getDocument(id);
		if (document != null) {
			ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
			
			// When an experiment is deleted, all other documents under it are deleted.
			artifactMetadataRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			dataProfileRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			dataResourceRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			runMetadataRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			shortReportRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			shortSchemaRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
			
			documentRepository.deleteById(id);
			return;
		}
		throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
	}
	
	// Delete
	public void deleteDocumentsByProjectId(String projectId, Optional<String> experimentId) {
		// When an experiment is deleted, all other documents under it are deleted.
		if (experimentId.isPresent()) {
			// If experimentId is present, delete all documents under that specific experiment.
			artifactMetadataRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			dataProfileRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			dataResourceRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			runMetadataRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			shortReportRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			shortSchemaRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
			
			documentRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
		} else {
			// If experimentId is not present, delete all experiments under the specified project and all documents under those experiments.
			artifactMetadataRepository.deleteByProjectId(projectId);
			dataProfileRepository.deleteByProjectId(projectId);
			dataResourceRepository.deleteByProjectId(projectId);
			runMetadataRepository.deleteByProjectId(projectId);
			shortReportRepository.deleteByProjectId(projectId);
			shortSchemaRepository.deleteByProjectId(projectId);
			
			documentRepository.deleteByProjectId(projectId);
		}
	}
}

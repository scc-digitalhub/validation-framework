package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.web.server.ResponseStatusException;

import it.smartcommunitylab.validationstorage.auth.SecurityAccessor;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class DataResourceService {
	private final DataResourceRepository documentRepository;
	private final SecurityAccessor securityAccessor;
	
	private DataResource getDocument(String id) {
		if (ObjectUtils.isEmpty(id))
			return null;
		
		Optional<DataResource> o = documentRepository.findById(id);
		if (o.isPresent()) {
			DataResource document = o.get();
			return document;
		}
		return null;
	}
	
	private List<DataResource> filterBySearchTerms(List<DataResource> items, String search) {
		return items;
	}
	
	// Create
	public DataResource createDocument(String projectId, DataResourceDTO request) {
		if (ObjectUtils.isEmpty(projectId))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Project ID is missing or blank.");
		securityAccessor.checkUserHasPermissions(projectId);
		
		String experimentId = request.getExperimentId();
		String runId = request.getRunId();
		
		if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Fields 'experiment_id', 'run_id' are required and cannot be blank.");
		
		if (!(documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId).isEmpty()))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document (project_id=" + projectId + ", experiment_id=" + experimentId + ", run_id=" + runId + ") already exists.");
		
		DataResource documentToSave = new DataResource(projectId, experimentId, runId);
		
		documentToSave.setExperimentName(request.getExperimentName());
		documentToSave.setContents(request.getContents());
		
		return documentRepository.save(documentToSave);
	}
	
	// Read
	public List<DataResource> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
		securityAccessor.checkUserHasPermissions(projectId);
		
		List<DataResource> repositoryResults;
		
		if (experimentId.isPresent() && runId.isPresent())
			repositoryResults = documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId.get(), runId.get());
		else if (experimentId.isPresent())
			repositoryResults = documentRepository.findByProjectIdAndExperimentId(projectId, experimentId.get());
		else if (runId.isPresent())
			repositoryResults = documentRepository.findByProjectIdAndRunId(projectId, runId.get());
		else
			repositoryResults = documentRepository.findByProjectId(projectId);
		
		if (search.isPresent())
			repositoryResults = filterBySearchTerms(repositoryResults, search.get());
		
		return repositoryResults;
	}
	
	// Read
	public DataResource findDocumentById(String projectId, String id) {
		DataResource document = getDocument(id);
		if (document != null) {
			securityAccessor.checkUserHasPermissions(document.getProjectId());
			
			ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
			
			return document;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
	}
	
	// Update
	public DataResource updateDocument(String projectId, String id, DataResourceDTO request) {
		if (ObjectUtils.isEmpty(id))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document ID is missing or blank.");
		
		DataResource document = getDocument(id);
		if (document == null)
			throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
		
		securityAccessor.checkUserHasPermissions(document.getProjectId());
		
		ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
		
		String experimentId = request.getExperimentId();
		String runId = request.getRunId();
		if ((experimentId != null && !(experimentId.equals(document.getExperimentId()))) || (runId != null && (!runId.equals(document.getRunId()))))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "A value was specified for experiment_id and/or run_id, but they do not match the values in the document with ID " + id + ". Are you sure you are trying to update the correct document?");
		
		document.setExperimentName(request.getExperimentName());
		document.setContents(request.getContents());
		
		return documentRepository.save(document);
	}
	
	// Delete
	public void deleteDocumentById(String projectId, String id) {
		DataResource document = getDocument(id);
		if (document != null) {
			securityAccessor.checkUserHasPermissions(document.getProjectId());
			
			ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
			
			documentRepository.deleteById(id);
			return;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
	}
	
	// Delete
	public void deleteDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId) {
		securityAccessor.checkUserHasPermissions(projectId);
		
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
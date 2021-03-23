package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.web.server.ResponseStatusException;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RunMetadataService {
	private final RunMetadataRepository documentRepository;
	
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
	
	// Create
	public RunMetadata createDocument(String projectId, RunMetadataDTO request) {
		if (ObjectUtils.isEmpty(projectId))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Project ID is missing or blank.");
		ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.CREATE, projectId);
		
		String experimentName = request.getExperimentName();
		String runId = request.getRunId();
		
		if ((ObjectUtils.isEmpty(experimentName)) || (ObjectUtils.isEmpty(runId)))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Fields 'experiment_name', 'run_id' are required and cannot be blank.");
		
		String id = ValidationStorageUtils.DATA_RESOURCE + '_' + projectId + '_' + experimentName + "_" + runId;
		
		if (getDocument(id) != null)
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document already exists. ID: " + id);
		
		RunMetadata documentToSave = new RunMetadata(projectId, experimentName, runId);
		documentToSave.setId(id);
		documentToSave.setContents(request.getContents());
		
		return documentRepository.save(documentToSave);
	}
	
	// Read
	public List<RunMetadata> findDocumentsByProjectId(String projectId, Optional<String> experimentName, Optional<String> runId) {
		ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.READ, projectId);
		
		if (experimentName.isPresent() && runId.isPresent())
			return documentRepository.findByProjectIdAndExperimentNameAndRunId(projectId, experimentName.get(), runId.get());
		else if (experimentName.isPresent())
			return documentRepository.findByProjectIdAndExperimentName(projectId, experimentName.get());
		else if (runId.isPresent())
			return documentRepository.findByProjectIdAndRunId(projectId, runId.get());
		else
			return documentRepository.findByProjectId(projectId);
	}
	
	// Read
	public RunMetadata findDocumentById(String id) {
		RunMetadata document = getDocument(id);
		if (document != null) {
			ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.READ, document.getProjectId());
			return document;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with id=" + id + " was not found.");
	}
	
	// Update
	public RunMetadata updateDocument(String id, RunMetadataDTO request) {
		if (ObjectUtils.isEmpty(id))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document ID is missing or blank.");
		
		RunMetadata documentToUpdate = getDocument(id);
		if (documentToUpdate == null)
			throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
		ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.UPDATE, documentToUpdate.getProjectId());
		
		String experimentName = request.getExperimentName();
		String runId = request.getRunId();
		if ((experimentName != null && experimentName != documentToUpdate.getExperimentName()) || (runId != null && runId != documentToUpdate.getRunId()))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "A value was specified for experiment_name and/or run_id, but they do not match the values in the document with ID " + id + ". Are you sure you are trying to update the correct document?");
		
		documentToUpdate.setContents(request.getContents());
		
		return documentRepository.save(documentToUpdate);
	}
	
	// Delete
	public void deleteDocumentById(String id) {
		RunMetadata document = getDocument(id);
		if (document != null) {
			ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.DELETE, document.getProjectId());
			documentRepository.deleteById(id);
			return;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
	}
	
	// Delete
		public void deleteDocumentsByProjectId(String projectId, Optional<String> experimentName, Optional<String> runId) {
			ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.DELETE, projectId);
			
			if (experimentName.isPresent() && runId.isPresent())
				documentRepository.deleteByProjectIdAndExperimentNameAndRunId(projectId, experimentName.get(), runId.get());
			else if (experimentName.isPresent())
				documentRepository.deleteByProjectIdAndExperimentName(projectId, experimentName.get());
			else if (runId.isPresent())
				documentRepository.deleteByProjectIdAndRunId(projectId, runId.get());
			else
				documentRepository.deleteByProjectId(projectId);
		}
	
}
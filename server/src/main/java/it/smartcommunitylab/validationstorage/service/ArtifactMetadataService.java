package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.web.server.ResponseStatusException;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ArtifactMetadataService {
	private final ArtifactMetadataRepository documentRepository;
	
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
	
	// Create
	public ArtifactMetadata createDocument(String projectId, ArtifactMetadataDTO request) {
		if (ObjectUtils.isEmpty(projectId))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Project ID is missing or blank.");
		ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.CREATE, projectId);
		
		String experimentName = request.getExperimentName();
		String runId = request.getRunId();
		String name = request.getName();
		String uri = request.getUri();
		
		if ((ObjectUtils.isEmpty(experimentName)) || (ObjectUtils.isEmpty(runId)) || (ObjectUtils.isEmpty(name)) || (ObjectUtils.isEmpty(uri)))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Fields 'experiment_name', 'run_id', 'name', 'uri' are required and cannot be blank.");
		
		ArtifactMetadata documentToSave = new ArtifactMetadata(projectId, experimentName, runId, name, uri);
		
		return documentRepository.save(documentToSave);
	}
	
	// Read
	public List<ArtifactMetadata> findDocumentsByProjectId(String projectId, Optional<String> experimentName, Optional<String> runId) {
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
	public ArtifactMetadata findDocumentById(String id) {
		ArtifactMetadata document = getDocument(id);
		if (document != null) {
			ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.READ, document.getProjectId());
			return document;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with id=" + id + " was not found.");
	}
	
	// Update
	public ArtifactMetadata updateDocument(String id, ArtifactMetadataDTO request) {
		if (ObjectUtils.isEmpty(id))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document ID is missing or blank.");
		
		ArtifactMetadata documentToUpdate = getDocument(id);
		if (documentToUpdate == null)
			throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
		ValidationStorageUtils.checkUserHasPermissions(ValidationStorageUtils.OperationType.UPDATE, documentToUpdate.getProjectId());
		
		documentToUpdate.setExperimentName(request.getExperimentName());
		documentToUpdate.setRunId(request.getRunId());
		documentToUpdate.setName(request.getName());
		documentToUpdate.setUri(request.getUri());
		
		return documentRepository.save(documentToUpdate);
	}
	
	// Delete
	public void deleteDocumentById(String id) {
		ArtifactMetadata document = getDocument(id);
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
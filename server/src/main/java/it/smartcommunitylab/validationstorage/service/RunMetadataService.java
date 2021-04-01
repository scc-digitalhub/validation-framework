package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.web.server.ResponseStatusException;

import it.smartcommunitylab.validationstorage.auth.SecurityAccessor;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RunMetadataService {
	private final RunMetadataRepository documentRepository;
	private final DataResourceRepository dataResourceRepository;
	private final ShortReportRepository shortReportRepository;
	private final ArtifactMetadataRepository artifactMetadataRepository;
	private final SecurityAccessor securityAccessor;
	
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
	
	private List<RunMetadata> filterBySearch(List<RunMetadata> items, String search) {
		if (ObjectUtils.isEmpty(search))
			return items;
		
		String normalized = ValidationStorageUtils.normalizeString(search);
		
		List<RunMetadata> results = new ArrayList<RunMetadata>();
		for (RunMetadata item : items) {
			if (item.getExperimentName().contains(normalized))
				results.add(item);
		}
		
		return results;
	}
	
	// Create
	public RunMetadata createDocument(String projectId, RunMetadataDTO request, Optional<String> overwriteParam) {
		if (ObjectUtils.isEmpty(projectId))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Project ID is missing or blank.");
		securityAccessor.checkUserHasPermissions(projectId);
		
		String experimentId = request.getExperimentId();
		String runId = request.getRunId();
		
		if ((ObjectUtils.isEmpty(experimentId)) || (ObjectUtils.isEmpty(runId)))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Fields 'experiment_id', 'run_id' are required and cannot be blank.");
		
		Boolean overwrite = false;
		if (overwriteParam.isPresent() && !(ObjectUtils.isEmpty(overwriteParam.get())) && (overwriteParam.get().equals("true")))
			overwrite = true;
		
		if ((!overwrite) && (!(documentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId).isEmpty())))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document (project_id=" + projectId + ", experiment_id=" + experimentId + ", run_id=" + runId + ") already exists.");
		else if (overwrite) {
			documentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
			dataResourceRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
			shortReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
			artifactMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
		}
		
		RunMetadata documentToSave = new RunMetadata(projectId, experimentId, runId);
		
		documentToSave.setExperimentName(request.getExperimentName());
		documentToSave.setContents(request.getContents());
		
		return documentRepository.save(documentToSave);
	}
	
	// Read
	public List<RunMetadata> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
		securityAccessor.checkUserHasPermissions(projectId);
		
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
			securityAccessor.checkUserHasPermissions(document.getProjectId());
			
			ValidationStorageUtils.checkProjectIdMatch(id, document.getProjectId(), projectId);
			
			return document;
		}
		throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Document with ID " + id + " was not found.");
	}
	
	// Update
	public RunMetadata updateDocument(String projectId, String id, RunMetadataDTO request) {
		if (ObjectUtils.isEmpty(id))
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Document ID is missing or blank.");
		
		RunMetadata document = getDocument(id);
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
		RunMetadata document = getDocument(id);
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
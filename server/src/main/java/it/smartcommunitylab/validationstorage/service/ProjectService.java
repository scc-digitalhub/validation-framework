package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.DataPackageRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.repository.StoreRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

@Service
public class ProjectService {
    @Autowired
    private ProjectRepository repository;
    
    @Autowired
    private ExperimentRepository experimentRepository;
    
    @Autowired
    private DataPackageRepository dataPackageRepository;
    
    @Autowired
    private StoreRepository storeRepository;
    
    private Project getProject(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Project> o = repository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    public ProjectDTO createProject(ProjectDTO request) {
        String id = request.getName();
        
        if (getProject(id) != null)
            throw new DocumentAlreadyExistsException("Document with name '" + id + "' already exists.");
            
        Project document = new Project();
        
        document.setName(id);
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        
        repository.save(document);
        
        return request;
    }
    
    @PostFilter(ValidationStorageConstants.POSTFILTER_ID)
    public List<ProjectDTO> findProjects() {
        List<ProjectDTO> dtos = new ArrayList<ProjectDTO>();
        
        Iterable<Project> results = repository.findAll();
        for (Project r : results) {
            dtos.add(ProjectDTO.from(r));
        }
        
        return dtos;
    }
    
    public ProjectDTO findProjectById(String id) {
        Project document = getProject(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return ProjectDTO.from(document);
    }
    
    public ProjectDTO updateProject(String id, ProjectDTO request) {
        Project document = getProject(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with name '" + id + "' was not found.");
        
        ValidationStorageUtils.checkIdMatch(id, request.getName());
        
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        
        repository.save(document);
        
        return request;
    }
    
    public void deleteProject(String id) {
        Project document = getProject(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with name '" + id + "' was not found.");
        // TODO delete experiments/runs/etc?
        repository.deleteById(id);
    }

//    @Autowired
//    private ExperimentRepository experimentRepository;
//    @Autowired
//    private ArtifactMetadataRepository artifactMetadataRepository;
//    @Autowired
//    private RunDataProfileRepository dataProfileRepository;
//    @Autowired
//    private RunDataResourceRepository dataResourceRepository;
//    @Autowired
//    private RunEnvironmentRepository runEnvironmentRepository;
//    @Autowired
//    private RunMetadataRepository runMetadataRepository;
//    @Autowired
//    private RunShortReportRepository shortReportRepository;
//    @Autowired
//    private RunShortSchemaRepository shortSchemaRepository;
//
//    /**
//     * Given an ID, returns the corresponding document, or null if it can't be found.
//     * 
//     * @param id ID of the document to retrieve.
//     * @return The document if found, null otherwise.
//     */
//    private Project getDocument(String id) {
//        if (ObjectUtils.isEmpty(id))
//            return null;
//
//        Optional<Project> o = documentRepository.findById(id);
//        if (o.isPresent()) {
//            Project document = o.get();
//            return document;
//        }
//        return null;
//    }
//
//    // Create
//    public Project createDocument(ProjectDTO request, String author) {
//        String projectId = request.getId();
//
//        if (ObjectUtils.isEmpty(projectId))
//            throw new IllegalArgumentException("Field 'id' is required and cannot be blank.");
//
//        if (getDocument(projectId) != null)
//            throw new DocumentAlreadyExistsException("Document (id=" + projectId + ") already exists.");
//
//        Project documentToSave = new Project();
//
//        documentToSave.setId(projectId);
//        documentToSave.setName(request.getName());
//        documentToSave.setAuthor(author);
//
//        return documentRepository.save(documentToSave);
//    }
//
//    // Read
//    public Project findDocumentById(String id) {
//        Project document = getDocument(id);
//        if (document != null)
//            return document;
//
//        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//    }
//
//    // Read
//    @PostFilter(ValidationStorageConstants.POSTFILTER_ID)
//    public List<Project> findDocuments() {
//        return documentRepository.findAll();
//    }
//
//    // Update
//    public Project updateDocument(String id, ProjectDTO request) {
//        if (ObjectUtils.isEmpty(id))
//            throw new IllegalArgumentException("Document ID is missing or blank.");
//
//        Project document = getDocument(id);
//        if (document == null)
//            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//
//        String requestProjectId = request.getId();
//        if (requestProjectId != null && !(id.equals(requestProjectId)))
//            throw new IllegalArgumentException("A value for the project ID was specified in the request, but it does not match the project ID in the path. Are you sure you are trying to update the correct document?");
//
//        document.setName(request.getName());
//
//        return documentRepository.save(document);
//    }
//
//    // Delete
//    public void deleteDocumentById(String id) {
//        Project document = getDocument(id);
//        if (document != null) {
//            // When a project is deleted, all other documents under it are deleted.
//            artifactMetadataRepository.deleteByProjectId(id);
//            dataProfileRepository.deleteByProjectId(id);
//            dataResourceRepository.deleteByProjectId(id);
//            runEnvironmentRepository.deleteByProjectId(id);
//            runMetadataRepository.deleteByProjectId(id);
//            shortReportRepository.deleteByProjectId(id);
//            shortSchemaRepository.deleteByProjectId(id);
//
//            experimentRepository.deleteByProjectId(id);
//
//            documentRepository.deleteById(id);
//
//            return;
//        }
//        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//    }
}
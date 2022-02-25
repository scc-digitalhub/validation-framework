package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

@Service
public class ProjectService {
    @Autowired
    private ProjectRepository repository;
    
    public ProjectDTO createProject(ProjectDTO request) {
     // TODO Auto-generated method stub
        return null;
    }
    
    public List<ProjectDTO> findProjects() {
        // TODO Auto-generated method stub
           return null;
       }
    
    public ProjectDTO findProjectById(String id) {
     // TODO Auto-generated method stub
        return null;
    }
    
    public ProjectDTO updateProject(String id, ProjectDTO request) {
     // TODO Auto-generated method stub
        return null;
    }
    
    public void deleteProject(String id) {
     // TODO Auto-generated method stub
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
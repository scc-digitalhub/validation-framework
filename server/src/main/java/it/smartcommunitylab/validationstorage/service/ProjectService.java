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
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
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
    private ExperimentService experimentService;
    
    @Autowired
    private DataResourceService dataResourceService;
    
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
        
        List<ExperimentDTO> experiments = experimentService.findExperiments(id);
        for (ExperimentDTO dto : experiments) {
            experimentService.deleteExperiment(id, dto.getId());
        }
        
        List<StoreDTO> stores = dataResourceService.findStores(id);
        for (StoreDTO dto : stores) {
            dataResourceService.deleteStore(id, dto.getId());
        }
        
        List<DataPackageDTO> packages = dataResourceService.findDataPackages(id);
        for (DataPackageDTO dto : packages) {
            dataResourceService.deleteDataPackage(id, dto.getId());
        }
        
        List<DataResourceDTO> resources = dataResourceService.findDataResources(id);
        for (DataResourceDTO dto : resources) {
            dataResourceService.deleteDataResource(id, dto.getId());
        }
        
        repository.deleteById(id);
    }

}
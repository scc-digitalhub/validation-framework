package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PostFilter;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.repository.ProjectRepository;

@Service
public class ProjectService {
    @Autowired
    private ProjectRepository repository;
    
    @Autowired
    private ExperimentService experimentService;
    
    @Autowired
    private DataResourceService dataResourceService;
    
    private Project searchProject(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Project> o = repository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Project retrieveProject(String id) {
        Project document = searchProject(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Project '" + id + "' was not found.");
        
        return document;
    }
    
    public ProjectDTO createProject(ProjectDTO request) {
        String id = request.getName();
        
        if (searchProject(id) != null)
            throw new DocumentAlreadyExistsException("Project '" + id + "' already exists.");
            
        Project document = new Project();
        
        document.setName(id);
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        
        document = repository.save(document);
        
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
    
    //@PostFilter(ValidationStorageConstants.POSTFILTER_ID)
    public Page<ProjectDTO> findProjects(Set<String> authorities, Pageable pageable) {
        Page<Project> documents = repository.findByNameIn(authorities, pageable);
        List<ProjectDTO> documentsList = documents.getContent().stream().map(ProjectDTO::from).collect(Collectors.toList());
        Page<ProjectDTO> results = new PageImpl<>(documentsList, documents.getPageable(), documents.getTotalElements());
        
        return results;
    }
    
    public ProjectDTO findProjectById(String id) {
        Project document = retrieveProject(id);
        
        return ProjectDTO.from(document);
    }
    
    public ProjectDTO updateProject(String id, ProjectDTO request) {
        Project document = retrieveProject(id);
        
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        
        document = repository.save(document);
        
        return request;
    }
    
    @Transactional
    public void deleteProject(String id) {
        retrieveProject(id);
        
        List<ExperimentDTO> experiments = experimentService.findExperiments(id);
        for (ExperimentDTO dto : experiments) {
            experimentService.deleteExperiment(id, dto.getName());
        }
        System.out.println("deleted experiments");
        List<StoreDTO> stores = dataResourceService.findStores(id);
        for (StoreDTO dto : stores) {
            dataResourceService.deleteStore(id, dto.getId());
        }
        System.out.println("deleted stores");
        List<DataPackageDTO> packages = dataResourceService.findDataPackages(id);
        for (DataPackageDTO dto : packages) {
            dataResourceService.deleteDataPackage(id, dto.getId());
        }
        System.out.println("deleted packages");
        List<DataResourceDTO> resources = dataResourceService.findDataResources(id);
        for (DataResourceDTO dto : resources) {
            dataResourceService.deleteDataResource(id, dto.getId());
        }
        System.out.println("deleted resources");
        repository.deleteById(id);
    }

}
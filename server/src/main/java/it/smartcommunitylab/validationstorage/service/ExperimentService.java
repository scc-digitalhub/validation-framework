package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.IdMismatchException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Project;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ConstraintRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.RunConfigRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

@Service
public class ExperimentService {
    @Autowired
    private ExperimentRepository experimentRepository;
    
    @Autowired
    private ConstraintRepository constraintRepository;
    
    @Autowired
    private RunConfigRepository runConfigRepository;
    /*
    @Autowired
    private RunRepository runRepository;*/
    
    private Experiment getExperiment(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Experiment> o = experimentRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Experiment getExperimentByName(String projectId, String name) {
        List<Experiment> l = experimentRepository.findByProjectIdAndName(projectId, name);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private Constraint getConstraint(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Constraint> o = constraintRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Constraint getConstraintByName(String projectId, String experimentId, String name) {
        List<Constraint> l = constraintRepository.findByProjectIdAndExperimentIdAndName(projectId, experimentId, name);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private RunConfig getRunConfig(String projectId, String experimentId) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId))
            return null;

        List<RunConfig> l = runConfigRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        if (!ObjectUtils.isEmpty(l)) {
            return l.get(0);
        }
        
        return null;
    }
    /*
    private Run getRun(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Run> o = runRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }*/
    
    // Experiment
    public ExperimentDTO createExperiment(String projectId, ExperimentDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        String id = request.getId();
        if (id != null) {
            if (getExperiment(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (getExperimentByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "' already exists.");

        Experiment document = new Experiment();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setName(name);
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setTags(request.getTags());
        
        RunConfigDTO runConfigDTO = request.getRunConfig();
        if (runConfigDTO != null) {
            ValidationStorageUtils.checkIdMatch(projectId, runConfigDTO.getProjectId());
            ValidationStorageUtils.checkIdMatch(id, runConfigDTO.getExperimentId());
            
            RunConfig runConfig = RunConfigDTO.to(request.getRunConfig());
            runConfig.setProjectId(projectId);
            runConfig.setExperimentId(id);
            
            System.out.println(runConfig);
            runConfigRepository.save(runConfig);
            
            document.setRunConfig(runConfig);
        }
        
        experimentRepository.save(document);
        
        return ExperimentDTO.from(document);
    }
    
    public List<ExperimentDTO> findExperiments(String projectId, Optional<String> experimentName) {
        List<ExperimentDTO> dtos = new ArrayList<ExperimentDTO>();

        Iterable<Experiment> results;
        if (experimentName.isPresent())
            results = experimentRepository.findByProjectIdAndName(projectId, experimentName.get());
        else
            results = experimentRepository.findByProjectId(projectId);

        for (Experiment r : results)
            dtos.add(ExperimentDTO.from(r));
            
        return dtos;
    }
   
    public ExperimentDTO findExperimentById(String projectId, String id) {
        Experiment document = getExperiment(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return ExperimentDTO.from(document);
    }
   
    public ExperimentDTO updateExperiment(String projectId, String id, ExperimentDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        Experiment document = getExperiment(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setTags(request.getTags());
        
        experimentRepository.save(document);
        
        return ExperimentDTO.from(document);
    }
   
    public void deleteExperiment(String projectId, String id) {
        Experiment document = getExperiment(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        // TODO delete runs/etc?
        experimentRepository.deleteById(id);
    }
    
    // Constraint
    public ConstraintDTO createConstraint(String projectId, String experimentId, ConstraintDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        
        String id = request.getId();
        if (id != null) {
            if (getConstraint(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (getConstraintByName(projectId, experimentId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "', experiment '" + experimentId + "' already exists.");

        Constraint document = new Constraint();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setName(name);
        document.setTitle(request.getTitle());
        document.setResourceIds(request.getResourceIds());
        document.setType(request.getConstraint().getType());
        document.setDescription(request.getDescription());
        document.setErrorSeverity(request.getErrorSeverity());
        document.setConstraint(request.getConstraint());
        
        constraintRepository.save(document);
        
        return ConstraintDTO.from(document);
    }
    
    public List<ConstraintDTO> findConstraints(String projectId, String experimentId) {
        List<ConstraintDTO> dtos = new ArrayList<ConstraintDTO>();

        Iterable<Constraint> results = constraintRepository.findByProjectIdAndExperimentId(projectId, experimentId);

        for (Constraint r : results)
            dtos.add(ConstraintDTO.from(r));
            
        return dtos;
    }
   
    public ConstraintDTO findConstraintById(String projectId, String experimentId, String id) {
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return ConstraintDTO.from(document);
    }
   
    public ConstraintDTO updateConstraint(String projectId, String experimentId, String id, ConstraintDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");

        document.setTitle(request.getTitle());
        document.setResourceIds(request.getResourceIds());
        document.setType(request.getConstraint().getType());
        document.setDescription(request.getDescription());
        document.setErrorSeverity(request.getErrorSeverity());
        document.setConstraint(request.getConstraint());
        
        constraintRepository.save(document);
        
        return ConstraintDTO.from(document);
    }
   
    public void deleteConstraint(String projectId, String experimentId, String id) {
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        // TODO delete other documents?
        constraintRepository.deleteById(id);
    }
    
    // RunConfig
    public RunConfigDTO createRunConfig(String projectId, String experimentId, RunConfigDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        
        if (getRunConfig(projectId, experimentId) != null)
            throw new DocumentAlreadyExistsException("Document for project '" + projectId + "', experiment '" + experimentId + "' already exists.");
        
        RunConfig document = RunConfigDTO.to(request);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        
        runConfigRepository.save(document);
        
        return RunConfigDTO.from(document);
    }
   
    public RunConfigDTO findRunConfig(String projectId, String experimentId) {
        RunConfig document = getRunConfig(projectId, experimentId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "' was not found.");
        
        return RunConfigDTO.from(document);
    }
   
    public RunConfigDTO updateRunConfig(String projectId, String experimentId, RunConfigDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        
        RunConfig document = getRunConfig(projectId, experimentId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "' was not found.");

        document.setSnapshot(request.getSnapshot());
        document.setProfiling(request.getProfiling());
        document.setSchemaInference(request.getSchemaInference());
        document.setValidation(request.getValidation());
        
        runConfigRepository.save(document);
        
        return RunConfigDTO.from(document);
    }
   
    public void deleteRunConfig(String projectId, String experimentId) {
        RunConfig document = getRunConfig(projectId, experimentId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "' was not found.");
        // TODO delete other documents?
        runConfigRepository.deleteByProjectIdAndExperimentId(projectId, experimentId);
    }

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
//    @Autowired
//    private ProjectService projectService;
//
//    /**
//     * Given an ID, returns the corresponding document, or null if it can't be found.
//     * 
//     * @param id ID of the document to retrieve.
//     * @return The document if found, null otherwise.
//     */
//    private Experiment getDocument(String id) {
//        if (ObjectUtils.isEmpty(id))
//            return null;
//
//        Optional<Experiment> o = documentRepository.findById(id);
//        if (o.isPresent()) {
//            Experiment document = o.get();
//            return document;
//        }
//        return null;
//    }
//
//    /**
//     * Filters a list by a term.
//     * 
//     * @param items  List to filter.
//     * @param search A term to filter results by.
//     * @return A new list, with only the results that found a match.
//     */
//    private List<Experiment> filterBySearch(List<Experiment> items, String search) {
//        if (ObjectUtils.isEmpty(search))
//            return items;
//
//        String normalized = ValidationStorageUtils.normalizeString(search);
//
//        List<Experiment> results = new ArrayList<Experiment>();
//        for (Experiment item : items) {
//            if (item.getExperimentName().toLowerCase().contains(normalized))
//                results.add(item);
//        }
//
//        return results;
//    }
//
//    // Create
//    public Experiment createDocument(String projectId, ExperimentDTO request, String author) {
//        if (ObjectUtils.isEmpty(projectId))
//            throw new IllegalArgumentException("Project ID is missing or blank.");
//        projectService.findDocumentById(projectId);
//
//        String experimentId = request.getExperimentId();
//
//        if (ObjectUtils.isEmpty(experimentId))
//            throw new IllegalArgumentException("Field 'experiment_id' is required and cannot be blank.");
//
//        if (!(documentRepository.findByProjectIdAndExperimentId(projectId, experimentId).isEmpty()))
//            throw new DocumentAlreadyExistsException("Document (projectId=" + projectId + ", experimentId=" + experimentId + ") already exists.");
//
//        Experiment documentToSave = new Experiment(projectId, experimentId);
//
//        documentToSave.setExperimentName(request.getExperimentName());
//        documentToSave.setTags(request.getTags());
//        documentToSave.setAuthor(author);
//
//        return documentRepository.save(documentToSave);
//    }
//    
//    /**
//     * Creates an experiment, if it does not already exist. Meant to be used by other services, when
//     * creating other documents, to automatically create the corresponding experiment if missing.
//     * 
//     * @param projectId ID of the project the experiment belongs to.
//     * @param experimentId ID of the experiment.
//     * @param experimentName Name of the experiment.
//     * @param author Author
//     */
//    void createExperimentIfMissing(String projectId, String experimentId, String experimentName, String author) {
//        if (documentRepository.findByProjectIdAndExperimentId(projectId, experimentId).size() == 0) {
//            Experiment experimentToSave = new Experiment(projectId, experimentId);
//            if (!ObjectUtils.isEmpty(experimentName))
//                experimentToSave.setExperimentName(experimentName);
//            if (!ObjectUtils.isEmpty(author))
//                experimentToSave.setAuthor(author);
//            documentRepository.save(experimentToSave);
//        }
//    }
//
//    // Read
//    public List<Experiment> findDocumentsByProjectId(String projectId, Optional<String> experimentId, Optional<String> search) {
//        List<Experiment> repositoryResults;
//
//        if (experimentId.isPresent())
//            repositoryResults = documentRepository.findByProjectIdAndExperimentId(projectId, experimentId.get());
//        else
//            repositoryResults = documentRepository.findByProjectId(projectId);
//
//        if (search.isPresent())
//            repositoryResults = filterBySearch(repositoryResults, search.get());
//
//        return repositoryResults;
//    }
//
//    // Read
//    public Experiment findDocumentById(String projectId, String id) {
//        Experiment document = getDocument(id);
//        if (document != null) {
//            if (!document.getProjectId().equals(projectId))
//                throw new IdMismatchException();
//
//            return document;
//        }
//        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//    }
//
//    // Update
//    public Experiment updateDocument(String projectId, String id, ExperimentDTO request) {
//        if (ObjectUtils.isEmpty(id))
//            throw new IllegalArgumentException("Document ID is missing or blank.");
//
//        Experiment document = getDocument(id);
//        if (document == null)
//            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//
//        if (!document.getProjectId().equals(projectId))
//            throw new IdMismatchException();
//
//        String experimentId = request.getExperimentId();
//        if (experimentId != null && !(experimentId.equals(document.getExperimentId())))
//            throw new IllegalArgumentException("A value was specified for experimentId, but does not match the value in the document with ID " + id + ". Are you sure you are trying to update the correct document?");
//
//        document.setExperimentName(request.getExperimentName());
//        document.setTags(request.getTags());
//
//        return documentRepository.save(document);
//    }
//
//    // Delete
//    public void deleteDocumentById(String projectId, String id) {
//        Experiment document = getDocument(id);
//        if (document != null) {
//            if (!document.getProjectId().equals(projectId))
//                throw new IdMismatchException();
//
//            // When an experiment is deleted, all other documents under it are deleted.
//            artifactMetadataRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            dataProfileRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            dataResourceRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            runEnvironmentRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            runMetadataRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            shortReportRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//            shortSchemaRepository.deleteByProjectIdAndExperimentId(projectId, document.getExperimentId());
//
//            documentRepository.deleteById(id);
//            return;
//        }
//        throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
//    }
//
//    // Delete
//    public void deleteDocumentsByProjectId(String projectId, Optional<String> experimentId) {
//        // When an experiment is deleted, all other documents under it are deleted.
//        if (experimentId.isPresent()) {
//            // If experimentId is present, delete all documents under that specific experiment.
//            artifactMetadataRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            dataProfileRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            dataResourceRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            runEnvironmentRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            runMetadataRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            shortReportRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//            shortSchemaRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//
//            documentRepository.deleteByProjectIdAndExperimentId(projectId, experimentId.get());
//        } else {
//            // If experimentId is not present, delete all experiments under the specified project and all documents under those experiments.
//            artifactMetadataRepository.deleteByProjectId(projectId);
//            dataProfileRepository.deleteByProjectId(projectId);
//            dataResourceRepository.deleteByProjectId(projectId);
//            runEnvironmentRepository.deleteByProjectId(projectId);
//            runMetadataRepository.deleteByProjectId(projectId);
//            shortReportRepository.deleteByProjectId(projectId);
//            shortSchemaRepository.deleteByProjectId(projectId);
//
//            documentRepository.deleteByProjectId(projectId);
//        }
//    }
}
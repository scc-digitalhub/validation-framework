package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import javax.transaction.Transactional;

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

    @Autowired
    private RunService runService;
    
    private Experiment getExperimentByName(String projectId, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(name))
            return null;

        Optional<Experiment> o = experimentRepository.findByProjectIdAndName(projectId, name);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Experiment getExperimentById(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Experiment> o = experimentRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private String getExperimentId(String projectId, String experimentName) {
        Experiment experiment = getExperimentByName(projectId, experimentName);
        return experiment.getId();
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
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId) || ObjectUtils.isEmpty(name))
            return null;
        
        List<Constraint> l = constraintRepository.findByProjectIdAndExperimentIdAndName(projectId, experimentId, name);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private RunConfig getExperimentRunConfig(String projectId, String experimentName) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentName))
            return null;
        
        Experiment e = getExperimentByName(projectId, experimentName);
        
        if (e == null)
            return null;
        
        return e.getRunConfig();
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
        
        String name = request.getName();
        if (getExperimentByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "' already exists.");
        
        String id = request.getId();
        if (id != null) {
            if (getExperimentById(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }

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
            
            RunConfig runConfig = RunConfigDTO.to(request.getRunConfig(), id);
            runConfig.setProjectId(projectId);
            
            runConfigRepository.save(runConfig);
            
            document.setRunConfig(runConfig);
        }
        
        experimentRepository.save(document);
        
        return ExperimentDTO.from(document);
    }
    
    public List<ExperimentDTO> findExperiments(String projectId) {
        List<ExperimentDTO> dtos = new ArrayList<ExperimentDTO>();

        Iterable<Experiment> results = experimentRepository.findByProjectId(projectId);

        for (Experiment r : results)
            dtos.add(ExperimentDTO.from(r));
            
        return dtos;
    }
   
    public ExperimentDTO findExperimentByName(String projectId, String name) {
        Experiment document = getExperimentByName(projectId, name);
        
        if (document == null)
            throw new DocumentNotFoundException("Document '" + name + "' under project '" + projectId + "' was not found.");
        
        return ExperimentDTO.from(document);
    }
   
    public ExperimentDTO updateExperiment(String projectId, String name, ExperimentDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        Experiment document = getExperimentByName(projectId, name);
        
        if (document == null)
            throw new DocumentNotFoundException("Document '" + name + "' under project '" + projectId + "' was not found.");
        
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setTags(request.getTags());
        
        experimentRepository.save(document);
        
        return ExperimentDTO.from(document);
    }
   
    @Transactional
    public void deleteExperiment(String projectId, String name) {
        Experiment document = getExperimentByName(projectId, name);
        
        if (document == null)
            throw new DocumentNotFoundException("Document '" + name + "' under project '" + projectId + "' was not found.");
        
        List<ConstraintDTO> constraints = findConstraints(projectId, name);
        for (ConstraintDTO dto : constraints) {
            deleteConstraint(projectId, name, dto.getId());
        }
        
        deleteExperimentRunConfig(projectId, name);
        
        List<RunDTO> runs = runService.findRuns(projectId, name);
        for (RunDTO dto : runs) {
            runService.deleteRun(projectId, name, dto.getId());
        }
        
        experimentRepository.deleteById(document.getId());
    }
    
    // Constraint
    public ConstraintDTO createConstraint(String projectId, String experimentName, ConstraintDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentName, request.getExperimentName());
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        String id = request.getId();
        if (id != null) {
            if (getConstraint(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (getConstraintByName(projectId, experimentId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "', experiment '" + experimentName + "' already exists.");

        Constraint document = new Constraint();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setName(name);
        document.setTitle(request.getTitle());
        document.setResources(request.getResources());
        document.setType(request.getTypedConstraint().getType());
        document.setDescription(request.getDescription());
        document.setWeight(request.getWeight());
        document.setTypedConstraint(request.getTypedConstraint());
        
        constraintRepository.save(document);
        
        return ConstraintDTO.from(document, experimentName);
    }
    
    public List<ConstraintDTO> findConstraints(String projectId, String experimentName) {
        List<ConstraintDTO> dtos = new ArrayList<ConstraintDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<Constraint> results = constraintRepository.findByProjectIdAndExperimentId(projectId, experimentId);

        for (Constraint r : results)
            dtos.add(ConstraintDTO.from(r, experimentName));
            
        return dtos;
    }
   
    public ConstraintDTO findConstraintById(String projectId, String experimentName, String id) {
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return ConstraintDTO.from(document, experimentName);
    }
   
    public ConstraintDTO updateConstraint(String projectId, String experimentName, String id, ConstraintDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentName, request.getExperimentName());
        
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");

        document.setTitle(request.getTitle());
        document.setResources(request.getResources());
        document.setType(request.getTypedConstraint().getType());
        document.setDescription(request.getDescription());
        document.setWeight(request.getWeight());
        document.setTypedConstraint(request.getTypedConstraint());
        
        constraintRepository.save(document);
        
        return ConstraintDTO.from(document, experimentName);
    }
   
    public void deleteConstraint(String projectId, String experimentName, String id) {
        Constraint document = getConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        constraintRepository.deleteById(id);
    }
    
    // RunConfig
    public RunConfigDTO createExperimentRunConfig(String projectId, String experimentName, RunConfigDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentName, request.getExperimentName());
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        if (getExperimentRunConfig(projectId, experimentName) != null)
            throw new DocumentAlreadyExistsException("Document for project '" + projectId + "', experiment '" + experimentName + "' already exists.");
        
        RunConfig document = RunConfigDTO.to(request, experimentId);
        document.setProjectId(projectId);
        
        runConfigRepository.save(document);
        
        Experiment experiment = getExperimentByName(projectId, experimentName);
        experiment.setRunConfig(document);
        experimentRepository.save(experiment);
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public RunConfigDTO findExperimentRunConfig(String projectId, String experimentName) {
        RunConfig document = getExperimentRunConfig(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentName + "' was not found.");
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public RunConfigDTO updateExperimentRunConfig(String projectId, String experimentName, RunConfigDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentName, request.getExperimentName());
        
        RunConfig document = getExperimentRunConfig(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentName + "' was not found.");

        document.setSnapshot(request.getSnapshot());
        document.setProfiling(request.getProfiling());
        document.setSchemaInference(request.getSchemaInference());
        document.setValidation(request.getValidation());
        
        runConfigRepository.save(document);
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public void deleteExperimentRunConfig(String projectId, String experimentName) {
        RunConfig document = getExperimentRunConfig(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentName + "' was not found.");
        
        Experiment experiment = getExperimentByName(projectId, experimentName);
        experiment.setRunConfig(null);
        experimentRepository.save(experiment);
        
        runConfigRepository.deleteById(document.getId());
    }

}
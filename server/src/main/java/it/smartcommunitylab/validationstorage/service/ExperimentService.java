package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.repository.ConstraintRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.RunConfigRepository;

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
    
    @Autowired
    private DataResourceService dataResourceService;
    
    private Experiment searchExperimentByName(String projectId, String experimentName) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentName))
            return null;

        Optional<Experiment> o = experimentRepository.findByProjectIdAndName(projectId, experimentName);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Experiment retrieveExperimentByName(String projectId, String experimentName) {
        Experiment document = searchExperimentByName(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Experiment '" + experimentName + "' under project '" + projectId + "' was not found.");
        
        return document;
    }
    
    private Experiment searchExperimentById(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Experiment> o = experimentRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private String getExperimentId(String projectId, String experimentName) {
        return retrieveExperimentByName(projectId, experimentName).getId();
    }
    
    private Constraint searchConstraint(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Constraint> o = constraintRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Constraint retrieveConstraint(String id) {
        Constraint document = searchConstraint(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Constraint '" + id + "' was not found.");
        
        return document;
    }
    
    private Constraint searchConstraintByName(String projectId, String experimentId, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId) || ObjectUtils.isEmpty(name))
            return null;
        
        List<Constraint> l = constraintRepository.findByProjectIdAndExperimentIdAndName(projectId, experimentId, name);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private RunConfig searchRunConfig(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunConfig> o = runConfigRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunConfig searchExperimentRunConfig(String projectId, String experimentName) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentName))
            return null;
        
        Experiment e = searchExperimentByName(projectId, experimentName);
        
        if (e == null)
            return null;
        
        return e.getRunConfig();
    }
    
    private RunConfig retrieveExperimentRunConfig(String projectId, String experimentName) {
        RunConfig document = searchExperimentRunConfig(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Config for experiment '" + experimentName + "' under project '" + projectId + "' was not found.");
        
        return document;
    }
    
    // Experiment
    public ExperimentDTO createExperiment(String projectId, ExperimentDTO request) {
        String name = request.getName();
        if (searchExperimentByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Experiment '" + name + "' under project '" + projectId + "' already exists.");
        
        String id = request.getId();
        if (id != null) {
            if (searchExperimentById(id) != null)
                throw new DocumentAlreadyExistsException("Experiment '" + id + "' already exists.");
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
            if(searchRunConfig(runConfigDTO.getId()) != null)
                throw new DocumentAlreadyExistsException("Config '" + runConfigDTO.getId() + "' already exists.");
            
            RunConfig runConfig = RunConfigDTO.to(runConfigDTO, projectId, id);
            
            runConfigRepository.save(runConfig);
            
            document.setRunConfig(runConfig);
        }
        
        DataPackageDTO dataPackageDTO = request.getDataPackage();
        DataPackage dataPackage = null;
        if (dataPackageDTO != null) {
            if (dataResourceService.searchDataPackage(dataPackageDTO.getId()) != null)
                throw new DocumentAlreadyExistsException("Package '" + dataPackageDTO.getId() + "' already exists.");
            
            dataPackage = DataPackageDTO.to(dataPackageDTO, projectId);
        } else {
            dataPackage = new DataPackage();
            
            dataPackage.setId(UUID.randomUUID().toString());
            dataPackage.setProjectId(projectId);
            dataPackage.setName(id);
            dataPackage.setTitle("Package for experiment " + id);
            dataPackage.setType("experiment");
        }
        
        dataPackage = dataResourceService.savePackageWithItsResources(dataPackage);
        document.setDataPackage(dataPackage);
        
        document = experimentRepository.save(document);
        
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
        Experiment document = retrieveExperimentByName(projectId, name);
        
        return ExperimentDTO.from(document);
    }
   
    public ExperimentDTO updateExperiment(String projectId, String name, ExperimentDTO request) {
        Experiment document = retrieveExperimentByName(projectId, name);
        
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setTags(request.getTags());
        
        document = experimentRepository.save(document);
        
        return ExperimentDTO.from(document);
    }
   
    @Transactional
    public void deleteExperiment(String projectId, String name) {
        Experiment document = retrieveExperimentByName(projectId, name);
        
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
        String experimentId = getExperimentId(projectId, experimentName);
        
        String id = request.getId();
        if (id != null) {
            if (searchConstraint(id) != null)
                throw new DocumentAlreadyExistsException("Constraint '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (searchConstraintByName(projectId, experimentId, name) != null)
            throw new DocumentAlreadyExistsException("Constraint '" + name + "' under project '" + projectId + "', experiment '" + experimentName + "' already exists.");

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
        
        document = constraintRepository.save(document);
        
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
        Constraint document = retrieveConstraint(id);
        
        return ConstraintDTO.from(document, experimentName);
    }
   
    public ConstraintDTO updateConstraint(String projectId, String experimentName, String id, ConstraintDTO request) {
        Constraint document = retrieveConstraint(id);

        document.setTitle(request.getTitle());
        document.setResources(request.getResources());
        document.setType(request.getTypedConstraint().getType());
        document.setDescription(request.getDescription());
        document.setWeight(request.getWeight());
        document.setTypedConstraint(request.getTypedConstraint());
        
        document = constraintRepository.save(document);
        
        return ConstraintDTO.from(document, experimentName);
    }
   
    public void deleteConstraint(String projectId, String experimentName, String id) {
        retrieveConstraint(id);
        
        constraintRepository.deleteById(id);
    }
    
    // RunConfig
    public RunConfigDTO createExperimentRunConfig(String projectId, String experimentName, RunConfigDTO request) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        if (searchExperimentRunConfig(projectId, experimentName) != null)
            throw new DocumentAlreadyExistsException("Config for project '" + projectId + "', experiment '" + experimentName + "' already exists.");
        
        RunConfig document = RunConfigDTO.to(request, projectId, experimentId);
        
        document = runConfigRepository.save(document);
        
        Experiment experiment = retrieveExperimentByName(projectId, experimentName);
        experiment.setRunConfig(document);
        experimentRepository.save(experiment);
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public RunConfigDTO findExperimentRunConfig(String projectId, String experimentName) {
        RunConfig document = retrieveExperimentRunConfig(projectId, experimentName);
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public RunConfigDTO updateExperimentRunConfig(String projectId, String experimentName, RunConfigDTO request) {
        RunConfig document = retrieveExperimentRunConfig(projectId, experimentName);

        document.setSnapshot(request.getSnapshot());
        document.setProfiling(request.getProfiling());
        document.setSchemaInference(request.getSchemaInference());
        document.setValidation(request.getValidation());
        
        document = runConfigRepository.save(document);
        
        return RunConfigDTO.from(document, experimentName);
    }
   
    public void deleteExperimentRunConfig(String projectId, String experimentName) {
        RunConfig document = retrieveExperimentRunConfig(projectId, experimentName);
        
        Experiment experiment = retrieveExperimentByName(projectId, experimentName);
        experiment.setRunConfig(null);
        experimentRepository.save(experiment);
        
        runConfigRepository.deleteById(document.getId());
    }

}
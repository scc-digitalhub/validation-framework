package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.RunConfigImpl;
import it.smartcommunitylab.validationstorage.model.RunDataProfile;
import it.smartcommunitylab.validationstorage.model.RunDataSchema;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.RunStatus;
import it.smartcommunitylab.validationstorage.model.RunValidationReport;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunValidationReportDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ConstraintRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.RunConfigRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

@Service
public class RunService {
    @Autowired
    private RunRepository runRepository;
    
    @Autowired
    private RunMetadataRepository runMetadataRepository;
    
    @Autowired
    private RunEnvironmentRepository runEnvironmentRepository;
    
    @Autowired
    private ArtifactMetadataRepository artifactMetadataRepository;
    
    @Autowired
    private RunDataProfileRepository runDataProfileRepository;
    
    @Autowired
    private RunValidationReportRepository runValidationReportRepository;
    
    @Autowired
    private RunDataSchemaRepository runDataSchemaRepository;
    
    @Autowired
    private ExperimentRepository experimentRepository;
    
    @Autowired
    private RunConfigRepository runConfigRepository;
    
    @Autowired
    private ConstraintRepository constraintRepository;
    
    private Experiment searchExperimentByName(String projectId, String experimentName) {
        if (projectId == null || experimentName == null)
            return null;
        
        Optional<Experiment> experiment = experimentRepository.findByProjectIdAndName(projectId, experimentName);
        
        if (experiment.isPresent())
            return experiment.get();
        
        return null;
    }
    
    private Experiment retrieveExperimentByName(String projectId, String experimentName) {
        Experiment document = searchExperimentByName(projectId, experimentName);
        
        if (document == null)
            throw new DocumentNotFoundException("Experiment '" + experimentName + "' under project '" + projectId + "' was not found.");
        
        return document;
    }
    
    private String getExperimentId(String projectId, String experimentName) {
        return retrieveExperimentByName(projectId, experimentName).getId();
    }
    
    private Run searchRun(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Run> o = runRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Run retrieveRun(String id) {
        Run document = searchRun(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Run '" + id + "' was not found.");
        
        return document;
    }
    
    private RunMetadata searchRunMetadata(String projectId, String experimentId, String runId) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId) || ObjectUtils.isEmpty(runId))
            return null;

        Optional<RunMetadata> document = runMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (document.isPresent()) {
            return document.get();
        }
        
        return null;
    }
    
    private RunMetadata retrieveRunMetadata(String projectId, String experimentId, String runId) {
        RunMetadata document = searchRunMetadata(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Metadata for project '" + projectId + "', experiment '" + experimentId + "', run '" + runId + "' was not found.");
        
        return document;
    }
    
    
    private RunEnvironment searchRunEnvironment(String projectId, String experimentId, String runId) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId) || ObjectUtils.isEmpty(runId))
            return null;

        Optional<RunEnvironment> document = runEnvironmentRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (document.isPresent()) {
            return document.get();
        }
        
        return null;
    }
    
    private RunEnvironment retrieveRunEnvironment(String projectId, String experimentId, String runId) {
        RunEnvironment document = searchRunEnvironment(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Environment for project '" + projectId + "', experiment '" + experimentId + "', run '" + runId + "' was not found.");
        
        return document;
    }
    
    private ArtifactMetadata searchArtifactMetadata(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<ArtifactMetadata> o = artifactMetadataRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private ArtifactMetadata retrieveArtifactMetadata(String id) {
        ArtifactMetadata document = searchArtifactMetadata(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Artifact '" + id + "' was not found.");
        
        return document;
    }
    
    private RunDataProfile searchRunDataProfile(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunDataProfile> o = runDataProfileRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunDataProfile retrieveRunDataProfile(String id) {
        RunDataProfile document = searchRunDataProfile(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Profile '" + id + "' was not found.");
        
        return document;
    }
    
    private RunValidationReport searchRunValidationReport(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunValidationReport> o = runValidationReportRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunValidationReport retrieveRunValidationReport(String id) {
        RunValidationReport document = searchRunValidationReport(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Validation report '" + id + "' was not found.");
        
        return document;
    }
    
    private RunDataSchema searchRunDataSchema(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunDataSchema> o = runDataSchemaRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunDataSchema retrieveRunDataSchema(String id) {
        RunDataSchema document = searchRunDataSchema(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Schema '" + id + "' was not found.");
        
        return document;
    }
    
    public RunConfig duplicateEnabledConfigs(RunConfig source) {
        RunConfig rc = new RunConfig();
        
        rc.setId(UUID.randomUUID().toString());
        rc.setProjectId(source.getProjectId());
        rc.setExperimentId(source.getExperimentId());
        
        List<RunConfigImpl> snapshot = new ArrayList<RunConfigImpl>();
        List<RunConfigImpl> profiling = new ArrayList<RunConfigImpl>();
        List<RunConfigImpl> schemaInference = new ArrayList<RunConfigImpl>();
        List<RunConfigImpl> validation = new ArrayList<RunConfigImpl>();
        
        if (source.getSnapshot() != null) {
            for (RunConfigImpl i : source.getSnapshot()) {
                if (i.isEnable()) {
                    snapshot.add(i);
                }
            }
        }
        
        if (source.getProfiling() != null) {
            for (RunConfigImpl i : source.getProfiling()) {
                if (i.isEnable()) {
                    profiling.add(i);
                }
            }
        }
        
        if (source.getSchemaInference() != null) {
            for (RunConfigImpl i : source.getSchemaInference()) {
                if (i.isEnable()) {
                    schemaInference.add(i);
                }
            }
        }
        
        if (source.getValidation() != null) {
            for (RunConfigImpl i : source.getValidation()) {
                if (i.isEnable()) {
                    validation.add(i);
                }
            }
        }
        
        if (!snapshot.isEmpty())
            rc.setSnapshot(snapshot);
        
        if (!profiling.isEmpty())
            rc.setProfiling(profiling);
        
        if (!schemaInference.isEmpty())
            rc.setSchemaInference(schemaInference);
        
        if (!validation.isEmpty())
            rc.setValidation(validation);
        
        return rc;
    }
    
    // Run
    /*
    public RunDTO createRun(String projectId, String experimentName, RunDTO request) {
        Experiment e = retrieveExperimentByName(projectId, experimentName);
        String experimentId = e.getId();
        
        String id = request.getId();
        if (id != null) {
            if (searchRun(id) != null)
                throw new DocumentAlreadyExistsException("Run '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        Run document = new Run();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunStatus(request.getRunStatus());
        
        // Build constraint map and recover all involved resources to create a package
        DataPackage dataPackage = null;
        List<ConstraintDTO> dtoConstraints = null;
        
        if (request.getConstraints() != null) {
            Map<String, TypedConstraint> typedConstraintMap = new HashMap<String, TypedConstraint>();
            Set<String> dataResourceIds = new HashSet<String>();
            
            // Recover constraints from DB
            List<Constraint> constraints = constraintRepository.findByProjectIdAndExperimentId(projectId, experimentId);
            Map<String, Constraint> constraintMap = new HashMap<String, Constraint>();
            for (Constraint c : constraints) {
                constraintMap.put(c.getName(), c);
            }
            
            dtoConstraints = new ArrayList<ConstraintDTO>();
            
            for (ConstraintDTO c : request.getConstraints()) {
                String constraintName = c.getName();
                Constraint dbConstraint = constraintMap.get(constraintName);
                typedConstraintMap.put(constraintName, dbConstraint.getTypedConstraint());
                dataResourceIds.addAll(dbConstraint.getResources());
                dtoConstraints.add(ConstraintDTO.from(dbConstraint, experimentName));
            }
            document.setConstraints(typedConstraintMap);
            
            Iterable<DataResource> dataResources = dataResourceRepository.findAllById(dataResourceIds);
            
            // Create run's package
            dataPackage = new DataPackage();
            dataPackage.setId(UUID.randomUUID().toString());
            dataPackage.setProjectId(projectId);
            dataPackage.setName(id);
            dataPackage.setTitle("Package for run " + id);
            dataPackage.setType("run");
            
            for (DataResource r : dataResources) {
                r.addPackage(dataPackage);
            }
            
            List<DataResource> dataResourcesList = new ArrayList<DataResource>();
            dataResources.forEach(dataResourcesList::add);
            dataPackage.setResources(dataResourcesList);
            
            dataPackageRepository.save(dataPackage);
            
            dataResourceRepository.saveAll(dataResources);
            
            // Set resources
            Map<String, DataResource> resourceMap = new HashMap<String, DataResource>();
            for (DataResource r : dataResources) {
                resourceMap.put(r.getName(), r);
            }
            document.setResources(resourceMap);
        }
        
        // Duplicate experiment's enabled configurations
        RunConfig rc = duplicateEnabledConfigs(e.getRunConfig());
        document.setRunConfig(rc);
        
        runConfigRepository.save(rc);
        
        document = runRepository.save(document);
        
        return RunDTO.from(document, experimentName, DataPackageDTO.from(dataPackage), dtoConstraints);
    }*/
    public RunDTO createRun(String projectId, String experimentName, RunDTO request) {

        Experiment e = retrieveExperimentByName(projectId, experimentName);
        String experimentId = e.getId();

        String id;
        if (request != null && request.getId() != null) {
            id = request.getId();
            if (searchRun(id) != null)
                throw new DocumentAlreadyExistsException("Run '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }

        Run document = new Run();

        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);

        RunStatus status = request != null && request.getRunStatus() != null ? request.getRunStatus()
                : RunStatus.PENDING;
        document.setRunStatus(status);
        
        // Config
        RunConfig rc;
        if (request != null && request.getRunConfig() != null) {
            rc = RunConfigDTO.to(request.getRunConfig(), projectId, experimentId);
        } else {
            rc = duplicateEnabledConfigs(e.getRunConfig());
        }
        
        document.setRunConfig(rc);
        
        // Resources
        List<DataResource> expResources = e.getDataPackage().getResources();
        List<DataResource> runResources = expResources;
        
        if (request != null && request.getDataPackage() != null) {
            Set<String> runResourceNames = request.getDataPackage().getResources().stream().map(r -> r.getName()).collect(Collectors.toSet());
            Set<String> experimentResourceNames = expResources.stream().map(r -> r.getName()).collect(Collectors.toSet());
            
            if (!experimentResourceNames.containsAll(runResourceNames)) {
                throw new IllegalArgumentException("One or more resources listed do not belong to this experiment.");
            }
            
            runResources = expResources.stream().filter(r -> runResourceNames.contains(r.getName())).collect(Collectors.toList());
        }
        
        Map<String, DataResource> resourcesMap = runResources.stream().collect(Collectors.toMap(r -> r.getName(), r -> r));

        document.setResources(resourcesMap);

        // Constraints are exclusively for validation
        if (rc.isValidationEnabled()) {
            List<Constraint> expConstraints = constraintRepository.findByProjectIdAndExperimentId(projectId, experimentId);
            List<Constraint> runConstraints = expConstraints;
    
            if (request != null && request.getConstraints() != null) {
                Set<String> runConstraintNames = request.getConstraints().stream().map(c -> c.getName()).collect(Collectors.toSet());
                Set<String> experimentConstraintNames = expConstraints.stream().map(c -> c.getName()).collect(Collectors.toSet());
                
                if (!experimentConstraintNames.containsAll(runConstraintNames)) {
                    throw new IllegalArgumentException("One or more constraints listed do not belong to this experiment.");
                }
                
                runConstraints = expConstraints.stream().filter(c -> runConstraintNames.contains(c.getName())).collect(Collectors.toList());
            }
            
            if (runConstraints.isEmpty()) {
                throw new IllegalArgumentException("Validation is enabled but no constraints are defined.");
            }
            
            Map<String, Constraint> constraintsMap = runConstraints.stream().collect(Collectors.toMap(c -> c.getName(), c -> c));

            document.setConstraints(constraintsMap);
        }

        runConfigRepository.save(rc);
        
        document = runRepository.save(document);

        return RunDTO.from(document, experimentName);
    }
    
    public List<RunDTO> findRuns(String projectId, String experimentName) {
        List<RunDTO> dtos = new ArrayList<RunDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<Run> results = runRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        if (!results.iterator().hasNext())
            return dtos;
        
        List<Constraint> constraints = constraintRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        Map<String, Constraint> constraintMap = new HashMap<String, Constraint>();
        for (Constraint c : constraints) {
            constraintMap.put(c.getName(), c);
        }

        for (Run r : results) {
            dtos.add(RunDTO.from(r, experimentName));
        }

        return dtos;
    }
    
    public Page<RunDTO> findRuns(String projectId, String experimentName, Pageable pageable) {
//        Page<Experiment> documents = experimentRepository.findByProjectId(projectId, pageable);
//        List<ExperimentDTO> documentsList = documents.getContent().stream().map(ExperimentDTO::from).collect(Collectors.toList());
//        Page<ExperimentDTO> results = new PageImpl<>(documentsList, documents.getPageable(), documents.getTotalElements());
//        
//        return results;
    }
   
    public RunDTO findRunById(String projectId, String experimentName, String id) {
        Run document = retrieveRun(id);
        
        return RunDTO.from(document, experimentName);
    }
    
    public RunDTO updateRun(String projectId, String experimentName, String id, RunDTO request) {
        Run document = retrieveRun(id);

        document.setRunStatus(request.getRunStatus());
        
        document = runRepository.save(document);
        
        return RunDTO.from(document, experimentName);
    }
   
    @Transactional
    public void deleteRun(String projectId, String experimentName, String id) {
        Run document = retrieveRun(id);
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        artifactMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, id);
        deleteRunDataProfiles(projectId, experimentName, id);
        deleteRunValidationReports(projectId, experimentName, id);
        deleteRunDataSchemas(projectId, experimentName, id);
        
        try {
            deleteRunMetadata(projectId, experimentName, id);
        } catch (DocumentNotFoundException e) {
            // No need to delete
        }
        
        try {
            deleteRunEnvironment(projectId, experimentName, id);
        } catch (DocumentNotFoundException e) {
            // No need to delete
        }
        
        runRepository.deleteById(id);
        
        runConfigRepository.deleteById(document.getRunConfig().getId());
        
    }
    
    // RunMetadata
    public RunMetadataDTO createRunMetadata(String projectId, String experimentName, String runId, RunMetadataDTO request) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        if (searchRunMetadata(projectId, experimentId, runId) != null)
            throw new DocumentAlreadyExistsException("Document for project '" + projectId + "', experiment '" + experimentName + "', run '" + runId + "' already exists.");
        
        String id = request.getId();
        if (id == null)
            id = UUID.randomUUID().toString();
        
        RunMetadata document = new RunMetadata();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunId(runId);
        document.setCreatedDate(request.getCreatedDate());
        document.setStartedDate(request.getStartedDate());
        document.setFinishedDate(request.getFinishedDate());
        document.setMetadata(request.getMetadata());
        document.setContents(request.getContents());
        
        document = runMetadataRepository.save(document);
        
        Run run = retrieveRun(runId);
        run.setRunMetadata(document);
        runRepository.save(run);
        
        return RunMetadataDTO.from(document, experimentName);
    }
   
    public RunMetadataDTO findRunMetadata(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        RunMetadata document = retrieveRunMetadata(projectId, experimentId, runId);
        
        return RunMetadataDTO.from(document, experimentName);
    }
   
    public RunMetadataDTO updateRunMetadata(String projectId, String experimentName, String runId, RunMetadataDTO request) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        RunMetadata document = retrieveRunMetadata(projectId, experimentId, runId);
        
        document.setCreatedDate(request.getCreatedDate());
        document.setStartedDate(request.getStartedDate());
        document.setFinishedDate(request.getFinishedDate());
        document.setMetadata(request.getMetadata());
        document.setContents(request.getContents());
        
        document = runMetadataRepository.save(document);
        
        return RunMetadataDTO.from(document, experimentName);
    }
    
    @Transactional
    public void deleteRunMetadata(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        retrieveRunMetadata(projectId, experimentId, runId);
        
        Run run = retrieveRun(runId);
        run.setRunMetadata(null);
        runRepository.save(run);
        
        runMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunEnvironment
    public RunEnvironmentDTO createRunEnvironment(String projectId, String experimentName, String runId, RunEnvironmentDTO request) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        if (searchRunEnvironment(projectId, experimentId, runId) != null)
            throw new DocumentAlreadyExistsException("Environment for project '" + projectId + "', experiment '" + experimentName + "', run '" + runId + "' already exists.");
        
        String id = request.getId();
        if (id == null)
            id = UUID.randomUUID().toString();
        
        RunEnvironment document = new RunEnvironment();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunId(runId);
        document.setDatajudgeVersion(request.getDatajudgeVersion());
        document.setContents(request.getContents());
        
        document = runEnvironmentRepository.save(document);
        
        Run run = retrieveRun(runId);
        run.setRunEnvironment(document);
        runRepository.save(run);
        
        return RunEnvironmentDTO.from(document, experimentName);
    }
   
    public RunEnvironmentDTO findRunEnvironment(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        RunEnvironment document = retrieveRunEnvironment(projectId, experimentId, runId);
        
        return RunEnvironmentDTO.from(document, experimentName);
    }
   
    public RunEnvironmentDTO updateRunEnvironment(String projectId, String experimentName, String runId, RunEnvironmentDTO request) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        RunEnvironment document = retrieveRunEnvironment(projectId, experimentId, runId);
        
        document.setDatajudgeVersion(request.getDatajudgeVersion());
        document.setContents(request.getContents());
        
        document = runEnvironmentRepository.save(document);
        
        return RunEnvironmentDTO.from(document, experimentName);
    }
   
    @Transactional
    public void deleteRunEnvironment(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        
        retrieveRunEnvironment(projectId, experimentId, runId);
        
        Run run = retrieveRun(runId);
        run.setRunEnvironment(null);
        runRepository.save(run);
        
        runEnvironmentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // ArtifactMetadata
    public ArtifactMetadataDTO createArtifactMetadata(String projectId, String experimentName, String runId, ArtifactMetadataDTO request) {
        String id = request.getId();
        if (id != null) {
            if (searchArtifactMetadata(id) != null)
                throw new DocumentAlreadyExistsException("Artifact '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        ArtifactMetadata document = new ArtifactMetadata();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunId(runId);
        document.setName(request.getName());
        document.setUri(request.getUri());
        
        document = artifactMetadataRepository.save(document);
        
        return ArtifactMetadataDTO.from(document, experimentName);
    }
    
    public List<ArtifactMetadataDTO> findArtifactMetadata(String projectId, String experimentName, String runId) {
        List<ArtifactMetadataDTO> dtos = new ArrayList<ArtifactMetadataDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<ArtifactMetadata> results = artifactMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);

        for (ArtifactMetadata r : results)
            dtos.add(ArtifactMetadataDTO.from(r, experimentName));

        return dtos;
    }
   
    public ArtifactMetadataDTO findArtifactMetadataById(String projectId, String experimentName, String runId, String id) {
        ArtifactMetadata document = retrieveArtifactMetadata(id);
        
        return ArtifactMetadataDTO.from(document, experimentName);
    }
   
    public ArtifactMetadataDTO updateArtifactMetadata(String projectId, String experimentName, String runId, String id, ArtifactMetadataDTO request) {
        ArtifactMetadata document = retrieveArtifactMetadata(id);
        
        document.setName(request.getName());
        document.setUri(request.getUri());
        
        document = artifactMetadataRepository.save(document);
        
        return ArtifactMetadataDTO.from(document, experimentName);
    }
   
    public void deleteArtifactMetadata(String projectId, String experimentName, String runId, String id) {
        retrieveArtifactMetadata(id);
        
        artifactMetadataRepository.deleteById(id);
    }
    
    // RunDataProfile
    public List<RunDataProfileDTO> createRunDataProfiles(String projectId, String experimentName, String runId, RunStatus result, List<RunDataProfileDTO> reports) {
        List<RunDataProfile> documents = new ArrayList<RunDataProfile>();
        List<RunDataProfileDTO> results = new ArrayList<RunDataProfileDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunDataProfileDTO dto : reports) {
            RunDataProfile document = new RunDataProfile();
            
            String id = dto.getId();
            if (id != null) {
                if (searchRunDataProfile(id) != null)
                    throw new DocumentAlreadyExistsException("Profile '" + id + "' already exists.");
            } else {
                runId = UUID.randomUUID().toString();
            }
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setResourceName(dto.getResourceName());
            document.setType(dto.getType());
            document.setMetadata(dto.getMetadata());
            document.setProfile(dto.getProfile());
            
            documents.add(document);
            
            results.add(RunDataProfileDTO.from(document, experimentName));
        }
        
        runDataProfileRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setProfileResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunDataProfileDTO> findRunDataProfiles(String projectId, String experimentName, String runId) {
        List<RunDataProfileDTO> dtos = new ArrayList<RunDataProfileDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<RunDataProfile> results = runDataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunDataProfile r : results) {
            dtos.add(RunDataProfileDTO.from(r, experimentName));
        }

        return dtos;
    }
    
    public RunDataProfileDTO findRunDataProfileById(String projectId, String experimentName, String runId, String id) {
        RunDataProfile document = retrieveRunDataProfile(id);
        
        return RunDataProfileDTO.from(document, experimentName);
    }
    
    public RunStatus findProfileResult(String projectId, String experimentName, String runId) {
        Optional<Run> o = runRepository.findById(runId);
        if (o.isPresent()) {
            return o.get().getProfileResult();
        } else {
            throw new DocumentNotFoundException("Run '" + runId + "' was not found.");
        }
    }
   
    @Transactional
    public List<RunDataProfileDTO> updateRunDataProfiles(String projectId, String experimentName, String runId, RunStatus result, List<RunDataProfileDTO> reports) {
        List<RunDataProfile> documents = new ArrayList<RunDataProfile>();
        List<RunDataProfileDTO> results = new ArrayList<RunDataProfileDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunDataProfileDTO dto : reports) {
            RunDataProfile document = new RunDataProfile();
            
            String id = dto.getId();
            if (id == null)
                runId = UUID.randomUUID().toString();
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setResourceName(dto.getResourceName());
            document.setType(dto.getType());
            document.setMetadata(dto.getMetadata());
            document.setProfile(dto.getProfile());
            
            documents.add(document);
            
            results.add(RunDataProfileDTO.from(document, experimentName));
        }
        
        runDataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runDataProfileRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setProfileResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    @Transactional
    public void deleteRunDataProfiles(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        runDataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunValidationReport
    public List<RunValidationReportDTO> createRunValidationReports(String projectId, String experimentName, String runId, RunStatus result, List<RunValidationReportDTO> reports) {
        List<RunValidationReport> documents = new ArrayList<RunValidationReport>();
        List<RunValidationReportDTO> results = new ArrayList<RunValidationReportDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunValidationReportDTO dto : reports) {
            RunValidationReport document = new RunValidationReport();
            
            String id = dto.getId();
            if (id != null) {
                if (searchRunValidationReport(id) != null)
                    throw new DocumentAlreadyExistsException("Validation report '" + runId + "' already exists.");
            } else {
                runId = UUID.randomUUID().toString();
            }
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setType(dto.getType());
            document.setConstraintName(dto.getConstraintName());
            document.setValid(dto.getValid());
            document.setMetadata(dto.getMetadata());
            document.setErrors(dto.getErrors());
            document.setContents(dto.getContents());
            
            documents.add(document);
            
            results.add(RunValidationReportDTO.from(document, experimentName));
        }
        
        runValidationReportRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setValidationResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunValidationReportDTO> findRunValidationReports(String projectId, String experimentName, String runId) {
        List<RunValidationReportDTO> dtos = new ArrayList<RunValidationReportDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<RunValidationReport> results = runValidationReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunValidationReport r : results) {
            dtos.add(RunValidationReportDTO.from(r, experimentName));
        }

        return dtos;
    }
    
    public RunValidationReportDTO findRunValidationReportById(String projectId, String experimentName, String runId, String id) {
        RunValidationReport document = retrieveRunValidationReport(id);
        
        return RunValidationReportDTO.from(document, experimentName);
    }
    
    public RunStatus findValidationResult(String projectId, String experimentName, String runId) {
        Optional<Run> o = runRepository.findById(runId);
        if (o.isPresent()) {
            return o.get().getValidationResult();
        } else {
            throw new DocumentNotFoundException("Run '" + runId + "' was not found.");
        }
    }
   
    @Transactional
    public List<RunValidationReportDTO> updateRunValidationReports(String projectId, String experimentName, String runId, RunStatus result, List<RunValidationReportDTO> reports) {
        List<RunValidationReport> documents = new ArrayList<RunValidationReport>();
        List<RunValidationReportDTO> results = new ArrayList<RunValidationReportDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunValidationReportDTO dto : reports) {
            RunValidationReport document = new RunValidationReport();
            
            String id = dto.getId();
            if (id == null)
                runId = UUID.randomUUID().toString();
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setType(dto.getType());
            document.setConstraintName(dto.getConstraintName());
            document.setValid(dto.getValid());
            document.setMetadata(dto.getMetadata());
            document.setErrors(dto.getErrors());
            document.setContents(dto.getContents());
            
            documents.add(document);
            
            results.add(RunValidationReportDTO.from(document, experimentName));
        }
        
        runValidationReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runValidationReportRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setValidationResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    @Transactional
    public void deleteRunValidationReports(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        runValidationReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunDataSchema
    public List<RunDataSchemaDTO> createRunDataSchemas(String projectId, String experimentName, String runId, RunStatus result, List<RunDataSchemaDTO> reports) {
        List<RunDataSchema> documents = new ArrayList<RunDataSchema>();
        List<RunDataSchemaDTO> results = new ArrayList<RunDataSchemaDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunDataSchemaDTO dto : reports) {
            RunDataSchema document = new RunDataSchema();
            
            String id = dto.getId();
            if (id != null) {
                if (searchRunDataSchema(id) != null)
                    throw new DocumentAlreadyExistsException("Schema '" + runId + "' already exists.");
            } else {
                runId = UUID.randomUUID().toString();
            }
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setResourceName(dto.getResourceName());
            document.setType(dto.getType());
            document.setMetadata(dto.getMetadata());
            document.setSchema(dto.getSchema());
            
            documents.add(document);
            
            results.add(RunDataSchemaDTO.from(document, experimentName));
        }
        
        runDataSchemaRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setSchemaResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunDataSchemaDTO> findRunDataSchemas(String projectId, String experimentName, String runId) {
        List<RunDataSchemaDTO> dtos = new ArrayList<RunDataSchemaDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);

        Iterable<RunDataSchema> results = runDataSchemaRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunDataSchema r : results) {
            dtos.add(RunDataSchemaDTO.from(r, experimentName));
        }

        return dtos;
    }
    
    public RunDataSchemaDTO findRunDataSchemaById(String projectId, String experimentName, String runId, String id) {
        RunDataSchema document = retrieveRunDataSchema(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Schema '" + id + "' was not found.");
        
        return RunDataSchemaDTO.from(document, experimentName);
    }
    
    public RunStatus findSchemaResult(String projectId, String experimentName, String runId) {
        Optional<Run> o = runRepository.findById(runId);
        if (o.isPresent()) {
            return o.get().getSchemaResult();
        } else {
            throw new DocumentNotFoundException("Run '" + runId + "' was not found.");
        }
    }
   
    @Transactional
    public List<RunDataSchemaDTO> updateRunDataSchemas(String projectId, String experimentName, String runId, RunStatus result, List<RunDataSchemaDTO> reports) {
        List<RunDataSchema> documents = new ArrayList<RunDataSchema>();
        List<RunDataSchemaDTO> results = new ArrayList<RunDataSchemaDTO>();
        
        String experimentId = getExperimentId(projectId, experimentName);
        
        for (RunDataSchemaDTO dto : reports) {
            RunDataSchema document = new RunDataSchema();
            
            String id = dto.getId();
            if (id == null)
                runId = UUID.randomUUID().toString();
            
            document.setId(id);
            document.setProjectId(projectId);
            document.setExperimentId(experimentId);
            document.setRunId(runId);
            document.setResourceName(dto.getResourceName());
            document.setType(dto.getType());
            document.setMetadata(dto.getMetadata());
            document.setSchema(dto.getSchema());
            
            documents.add(document);
            
            results.add(RunDataSchemaDTO.from(document, experimentName));
        }
        
        runDataSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runDataSchemaRepository.saveAll(documents);
        
        Run run = runRepository.findById(runId).get();
        run.setSchemaResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    @Transactional
    public void deleteRunDataSchemas(String projectId, String experimentName, String runId) {
        String experimentId = getExperimentId(projectId, experimentName);
        runDataSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
}
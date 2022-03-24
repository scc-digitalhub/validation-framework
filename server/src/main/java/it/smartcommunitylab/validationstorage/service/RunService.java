package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Experiment;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.RunDataProfile;
import it.smartcommunitylab.validationstorage.model.RunDataSchema;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.RunStatus;
import it.smartcommunitylab.validationstorage.model.RunValidationReport;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.ProfileResultDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunValidationReportDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ExperimentRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;
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
    private ExperimentService experimentService;
    
    private Run getRun(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Run> o = runRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunMetadata getRunMetadata(String projectId, String experimentId, String runId) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(runId))
            return null;

        List<RunMetadata> l = runMetadataRepository.findByProjectIdAndRunId(projectId, runId);
        if (!ObjectUtils.isEmpty(l)) {
            return l.get(0);
        }
        
        return null;
    }
    
    private RunEnvironment getRunEnvironment(String projectId, String experimentId, String runId) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(runId))
            return null;

        List<RunEnvironment> l = runEnvironmentRepository.findByProjectIdAndRunId(projectId, runId);
        if (!ObjectUtils.isEmpty(l)) {
            return l.get(0);
        }
        
        return null;
    }
    
    private ArtifactMetadata getArtifactMetadata(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<ArtifactMetadata> o = artifactMetadataRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunDataProfile getRunDataProfile(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunDataProfile> o = runDataProfileRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunValidationReport getRunValidationReport(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunValidationReport> o = runValidationReportRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private RunDataSchema getRunDataSchema(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<RunDataSchema> o = runDataSchemaRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    // Run
    public RunDTO createRun(String projectId, String experimentId, RunDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        
        String id = request.getId();
        if (id != null) {
            if (getRun(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        Optional<Experiment> o = experimentRepository.findById(request.getExperimentId());
        Experiment experiment = o.get();
        
        Run document = new Run();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunConfig(experiment.getRunConfig());
        
        Map<String, DataResource> resourceMap = new HashMap<String, DataResource>();
        for (DataResourceDTO r : request.getDataPackage().getResources())
            resourceMap.put(r.getId(), DataResourceDTO.to(r));
        document.setResources(resourceMap);
        
        Map<String, TypedConstraint> constraintMap = new HashMap<String, TypedConstraint>();
        for (ConstraintDTO c : request.getConstraints())
            constraintMap.put(c.getId(), c.getConstraint());
        document.setConstraints(constraintMap);
        
        document.setRunStatus(request.getRunStatus());
        
        runRepository.save(document);
        
        return RunDTO.from(document, request.getDataPackage(), request.getConstraints());
    }
    
    public List<RunDTO> findRuns(String projectId, String experimentId) {
        List<RunDTO> dtos = new ArrayList<RunDTO>();

        Iterable<Run> results = runRepository.findByProjectIdAndExperimentId(projectId, experimentId);
        
        DataPackageDTO packageDTO = DataPackageDTO.from(experimentRepository.findById(experimentId).get().getDataPackage());
        List<ConstraintDTO> constraints = experimentService.findConstraints(projectId, experimentId);

        for (Run r : results) {
            dtos.add(RunDTO.from(r, packageDTO, constraints));
        }

        return dtos;
    }
   
    public RunDTO findRunById(String projectId, String experimentId, String id) {
        Run document = getRun(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        DataPackageDTO packageDTO = DataPackageDTO.from(experimentRepository.findById(experimentId).get().getDataPackage());
        List<ConstraintDTO> constraints = experimentService.findConstraints(projectId, experimentId);
        
        return RunDTO.from(document, packageDTO, constraints);
    }
   
    public void deleteRun(String projectId, String experimentId, String id) {
        Run document = getRun(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");

        /* TODO
        deleteRunMetadata(projectId, experimentId, id);
        deleteRunEnvironment(projectId, experimentId, id);
        artifactMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, id);
        deleteRunDataProfiles(projectId, experimentId, id);
        deleteRunValidationReports(projectId, experimentId, id);
        deleteRunDataSchemas(projectId, experimentId, id);
        */
        
        runRepository.deleteById(id);
    }
    
    // RunMetadata
    public RunMetadataDTO createRunMetadata(String projectId, String experimentId, String runId, RunMetadataDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        if (getRunMetadata(projectId, experimentId, runId) != null)
            throw new DocumentAlreadyExistsException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' already exists.");
        
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
        document.setStatus(request.getStatus());
        document.setMetadata(request.getMetadata());
        document.setContents(request.getContents());
        
        runMetadataRepository.save(document);
        
        return RunMetadataDTO.from(document);
    }
   
    public RunMetadataDTO findRunMetadata(String projectId, String experimentId, String runId) {
        RunMetadata document = getRunMetadata(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' was not found.");
        
        return RunMetadataDTO.from(document);
    }
   
    public RunMetadataDTO updateRunMetadata(String projectId, String experimentId, String runId, RunMetadataDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        RunMetadata document = getRunMetadata(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', run '" + runId + "' was not found.");

        document.setCreatedDate(request.getCreatedDate());
        document.setStartedDate(request.getStartedDate());
        document.setFinishedDate(request.getFinishedDate());
        document.setStatus(request.getStatus());
        document.setMetadata(request.getMetadata());
        document.setContents(request.getContents());
        
        runMetadataRepository.save(document);
        
        return RunMetadataDTO.from(document);
    }
    
    public void deleteRunMetadata(String projectId, String experimentId, String runId) {
        RunMetadata document = getRunMetadata(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' was not found.");
        runMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunEnvironment
    public RunEnvironmentDTO createRunEnvironment(String projectId, String experimentId, String runId, RunEnvironmentDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        if (getRunEnvironment(projectId, experimentId, runId) != null)
            throw new DocumentAlreadyExistsException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' already exists.");
        
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
        
        runEnvironmentRepository.save(document);
        
        return RunEnvironmentDTO.from(document);
    }
   
    public RunEnvironmentDTO findRunEnvironment(String projectId, String experimentId, String runId) {
        RunEnvironment document = getRunEnvironment(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' was not found.");
        
        return RunEnvironmentDTO.from(document);
    }
   
    public RunEnvironmentDTO updateRunEnvironment(String projectId, String experimentId, String runId, RunEnvironmentDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        RunEnvironment document = getRunEnvironment(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', run '" + runId + "' was not found.");

        document.setDatajudgeVersion(request.getDatajudgeVersion());
        document.setContents(request.getContents());
        
        runEnvironmentRepository.save(document);
        
        return RunEnvironmentDTO.from(document);
    }
   
    public void deleteRunEnvironment(String projectId, String experimentId, String runId) {
        RunEnvironment document = getRunEnvironment(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document for project '" + projectId + "', experiment '" + experimentId + "', runId '" + runId + "' was not found.");
        runEnvironmentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // ArtifactMetadata
    public ArtifactMetadataDTO createArtifactMetadata(String projectId, String experimentId, String runId, ArtifactMetadataDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        String id = request.getId();
        if (id != null) {
            if (getArtifactMetadata(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        ArtifactMetadata document = new ArtifactMetadata();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setExperimentId(experimentId);
        document.setRunId(runId);
        document.setName(request.getName());
        document.setUri(request.getUri());
        
        artifactMetadataRepository.save(document);
        
        return ArtifactMetadataDTO.from(document);
    }
    
    public List<ArtifactMetadataDTO> findArtifactMetadata(String projectId, String experimentId, String runId) {
        List<ArtifactMetadataDTO> dtos = new ArrayList<ArtifactMetadataDTO>();

        Iterable<ArtifactMetadata> results = artifactMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);

        for (ArtifactMetadata r : results)
            dtos.add(ArtifactMetadataDTO.from(r));

        return dtos;
    }
   
    public ArtifactMetadataDTO findArtifactMetadataById(String projectId, String experimentId, String runId, String id) {
        ArtifactMetadata document = getArtifactMetadata(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return ArtifactMetadataDTO.from(document);
    }
   
    public ArtifactMetadataDTO updateArtifactMetadata(String projectId, String experimentId, String runId, String id, ArtifactMetadataDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, request.getExperimentId());
        ValidationStorageUtils.checkIdMatch(runId, request.getRunId());
        
        ArtifactMetadata document = getArtifactMetadata(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");

        document.setName(request.getName());
        document.setUri(request.getUri());
        
        artifactMetadataRepository.save(document);
        
        return ArtifactMetadataDTO.from(document);
    }
   
    public void deleteArtifactMetadata(String projectId, String experimentId, String runId, String id) {
        ArtifactMetadata document = getArtifactMetadata(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        artifactMetadataRepository.deleteById(id);
    }
    
    // RunDataProfile
    public List<RunDataProfileDTO> createRunDataProfiles(String projectId, String experimentId, String runId, RunStatus result, List<RunDataProfileDTO> reports) {
        List<RunDataProfile> documents = new ArrayList<RunDataProfile>();
        List<RunDataProfileDTO> results = new ArrayList<RunDataProfileDTO>();
        
        for (RunDataProfileDTO dto : reports) {
            RunDataProfile document = new RunDataProfile();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
            String id = dto.getId();
            if (id != null) {
                if (getRunDataProfile(id) != null)
                    throw new DocumentAlreadyExistsException("Document with id '" + runId + "' already exists.");
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
            
            results.add(RunDataProfileDTO.from(document));
        }
        
        runDataProfileRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setProfileResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunDataProfileDTO> findRunDataProfiles(String projectId, String experimentId, String runId) {
        List<RunDataProfileDTO> dtos = new ArrayList<RunDataProfileDTO>();

        Iterable<RunDataProfile> results = runDataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunDataProfile r : results) {
            dtos.add(RunDataProfileDTO.from(r));
        }

        return dtos;
    }
    
    public RunDataProfileDTO findRunDataProfileById(String projectId, String experimentId, String runId, String id) {
        RunDataProfile document = getRunDataProfile(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return RunDataProfileDTO.from(document);
    }
    
    public RunStatus findProfileResult(String projectId, String experimentId, String runId) {
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        return run.getProfileResult();
    }
   
    public List<RunDataProfileDTO> updateRunDataProfiles(String projectId, String experimentId, String runId, RunStatus result, List<RunDataProfileDTO> reports) {
        List<RunDataProfile> documents = new ArrayList<RunDataProfile>();
        List<RunDataProfileDTO> results = new ArrayList<RunDataProfileDTO>();
        
        for (RunDataProfileDTO dto : reports) {
            RunDataProfile document = new RunDataProfile();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
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
            
            results.add(RunDataProfileDTO.from(document));
        }
        
        runDataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runDataProfileRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setProfileResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    public void deleteRunDataProfiles(String projectId, String experimentId, String runId) {
        runDataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunValidationReport
    public List<RunValidationReportDTO> createRunValidationReports(String projectId, String experimentId, String runId, RunStatus result, List<RunValidationReportDTO> reports) {
        List<RunValidationReport> documents = new ArrayList<RunValidationReport>();
        List<RunValidationReportDTO> results = new ArrayList<RunValidationReportDTO>();
        
        for (RunValidationReportDTO dto : reports) {
            RunValidationReport document = new RunValidationReport();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
            String id = dto.getId();
            if (id != null) {
                if (getRunValidationReport(id) != null)
                    throw new DocumentAlreadyExistsException("Document with id '" + runId + "' already exists.");
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
            
            results.add(RunValidationReportDTO.from(document));
        }
        
        runValidationReportRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setValidationResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunValidationReportDTO> findRunValidationReports(String projectId, String experimentId, String runId) {
        List<RunValidationReportDTO> dtos = new ArrayList<RunValidationReportDTO>();

        Iterable<RunValidationReport> results = runValidationReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunValidationReport r : results) {
            dtos.add(RunValidationReportDTO.from(r));
        }

        return dtos;
    }
    
    public RunValidationReportDTO findRunValidationReportById(String projectId, String experimentId, String runId, String id) {
        RunValidationReport document = getRunValidationReport(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return RunValidationReportDTO.from(document);
    }
    
    public RunStatus findValidationResult(String projectId, String experimentId, String runId) {
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        return run.getValidationResult();
    }
   
    public List<RunValidationReportDTO> updateRunValidationReports(String projectId, String experimentId, String runId, RunStatus result, List<RunValidationReportDTO> reports) {
        List<RunValidationReport> documents = new ArrayList<RunValidationReport>();
        List<RunValidationReportDTO> results = new ArrayList<RunValidationReportDTO>();
        
        for (RunValidationReportDTO dto : reports) {
            RunValidationReport document = new RunValidationReport();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
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
            
            results.add(RunValidationReportDTO.from(document));
        }
        
        runValidationReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runValidationReportRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setValidationResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    public void deleteRunValidationReports(String projectId, String experimentId, String runId) {
        runValidationReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunDataSchema
    public List<RunDataSchemaDTO> createRunDataSchemas(String projectId, String experimentId, String runId, RunStatus result, List<RunDataSchemaDTO> reports) {
        List<RunDataSchema> documents = new ArrayList<RunDataSchema>();
        List<RunDataSchemaDTO> results = new ArrayList<RunDataSchemaDTO>();
        
        for (RunDataSchemaDTO dto : reports) {
            RunDataSchema document = new RunDataSchema();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
            String id = dto.getId();
            if (id != null) {
                if (getRunDataSchema(id) != null)
                    throw new DocumentAlreadyExistsException("Document with id '" + runId + "' already exists.");
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
            
            results.add(RunDataSchemaDTO.from(document));
        }
        
        runDataSchemaRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setSchemaResult(result);
        runRepository.save(run);
        
        return results;
    }
    
    public List<RunDataSchemaDTO> findRunDataSchemas(String projectId, String experimentId, String runId) {
        List<RunDataSchemaDTO> dtos = new ArrayList<RunDataSchemaDTO>();

        Iterable<RunDataSchema> results = runDataSchemaRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        
        for (RunDataSchema r : results) {
            dtos.add(RunDataSchemaDTO.from(r));
        }

        return dtos;
    }
    
    public RunDataSchemaDTO findRunDataSchemaById(String projectId, String experimentId, String runId, String id) {
        RunDataSchema document = getRunDataSchema(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        return RunDataSchemaDTO.from(document);
    }
    
    public RunStatus findSchemaResult(String projectId, String experimentId, String runId) {
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        return run.getSchemaResult();
    }
   
    public List<RunDataSchemaDTO> updateRunDataSchemas(String projectId, String experimentId, String runId, RunStatus result, List<RunDataSchemaDTO> reports) {
        List<RunDataSchema> documents = new ArrayList<RunDataSchema>();
        List<RunDataSchemaDTO> results = new ArrayList<RunDataSchemaDTO>();
        
        for (RunDataSchemaDTO dto : reports) {
            RunDataSchema document = new RunDataSchema();
            
            ValidationStorageUtils.checkIdMatch(projectId, dto.getProjectId());
            ValidationStorageUtils.checkIdMatch(experimentId, dto.getExperimentId());
            ValidationStorageUtils.checkIdMatch(runId, dto.getRunId());
            
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
            
            results.add(RunDataSchemaDTO.from(document));
        }
        
        runDataSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        runDataSchemaRepository.saveAll(documents);
        
        Run run = runRepository.findByProjectIdAndExperimentIdAndId(projectId, experimentId, runId).get(0);
        run.setSchemaResult(result);
        runRepository.save(run);
        
        return results;
    }
   
    public void deleteRunDataSchemas(String projectId, String experimentId, String runId) {
        runDataSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
}

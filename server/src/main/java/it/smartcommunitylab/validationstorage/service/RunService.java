package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.ArtifactMetadata;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.RunDataProfile;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.model.dto.ProfileResultDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunValidationReportDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataSchemaDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunRepository;
import it.smartcommunitylab.validationstorage.repository.RunValidationReportRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataSchemaRepository;

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

    private RunDTO makeDTO(Run source) {
        RunDTO dto = new RunDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setRunConfig(ExperimentService.makeDTO(source.getRunConfig()));
        dto.setConstraints(null);
        dto.setResources(null);
        
        return dto;
    }
    
    private RunMetadataDTO makeDTO(RunMetadata source) {
        RunMetadataDTO dto = new RunMetadataDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setRunId(source.getRunId());
        dto.setCreated(source.getCreated());
        dto.setContents(source.getContents());
        
        return dto;
    }
    
    private RunEnvironmentDTO makeDTO(RunEnvironment source) {
        RunEnvironmentDTO dto = new RunEnvironmentDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setExperimentId(source.getExperimentId());
        dto.setRunId(source.getRunId());
        dto.setContents(source.getContents());
        
        return dto;
    }
    
    // Run
    public RunDTO createRun(String projectId, String experimentId, RunDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDTO> findRuns(String projectId, String experimentId) {
        List<RunDTO> dtos = new ArrayList<RunDTO>();

        Iterable<Run> results = runRepository.findByProjectIdAndExperimentId(projectId, experimentId);

        for (Run r : results)
            dtos.add(makeDTO(r));
            
        return dtos;
    }
   
    public RunDTO findRunById(String projectId, String experimentId, String id) {
        Run document = getRun(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        ValidationStorageUtils.checkIdMatch(projectId, document.getProjectId());
        ValidationStorageUtils.checkIdMatch(experimentId, document.getExperimentId());
        
        return makeDTO(document);
    }
   
    public void deleteRun(String projectId, String experimentId, String id) {
        runRepository.deleteById(id);
    }
    
    // RunMetadata
    public RunMetadataDTO createRunMetadata(String projectId, String experimentId, String runId, RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunMetadataDTO findRunMetadata(String projectId, String experimentId, String runId) {
        RunMetadata document = getRunMetadata(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + " was not found.");
        
        return makeDTO(document);
    }
   
    public RunMetadataDTO updateRunMetadata(String projectId, String experimentId, String runId, RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public void deleteRunMetadata(String projectId, String experimentId, String runId) {
        runMetadataRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunEnvironment
    public RunEnvironmentDTO createRunEnvironment(String projectId, String experimentId, String runId, RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunEnvironmentDTO findRunEnvironment(String projectId, String experimentId, String runId) {
        RunEnvironment document = getRunEnvironment(projectId, experimentId, runId);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with projectId=" + projectId + ", experimentId=" + experimentId + ", runId=" + runId + " was not found.");
        
        return makeDTO(document);
    }
   
    public RunEnvironmentDTO updateRunEnvironment(String projectId, String experimentId, String runId, RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunEnvironment(String projectId, String experimentId, String runId) {
        runEnvironmentRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // ArtifactMetadata
    public ArtifactMetadataDTO createArtifactMetadata(ArtifactMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public ArtifactMetadataDTO findArtifactMetadataById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public ArtifactMetadataDTO updateArtifactMetadata(String id, ArtifactMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteArtifactMetadata(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunDataProfile
    public List<RunDataProfileDTO> createRunDataProfiles(String projectId, String experimentId, String runId, String result, List<RunDataProfileDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDataProfileDTO> findRunDataProfiles(String projectId, String experimentId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunDataProfileDTO findRunDataProfileById(String projectId, String experimentId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findProfileResult(String projectId, String experimentId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunDataProfileDTO> updateRunDataProfiles(String projectId, String experimentId, String runId, String result, List<RunDataProfileDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataProfiles(String projectId, String experimentId, String runId) {
        runDataProfileRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunValidationReport
    public List<RunValidationReportDTO> createRunValidationReports(String projectId, String experimentId, String runId, String result, List<RunValidationReportDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunValidationReportDTO> findRunValidationReports(String projectId, String experimentId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunValidationReportDTO findRunValidationReportById(String projectId, String experimentId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findValidationResult(String projectId, String experimentId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunValidationReportDTO> updateRunValidationReports(String projectId, String experimentId, String runId, String result, List<RunValidationReportDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunValidationReports(String projectId, String experimentId, String runId) {
        runValidationReportRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
    
    // RunDataSchema
    public List<RunDataSchemaDTO> createRunDataSchemas(String projectId, String experimentId, String runId, String result, List<RunDataSchemaDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDataSchemaDTO> findRunDataSchemas(String projectId, String experimentId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunDataSchemaDTO findRunDataSchemaById(String projectId, String experimentId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findSchemaResult(String projectId, String experimentId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunDataSchemaDTO> updateRunDataSchemas(String projectId, String experimentId, String runId, String result, List<RunDataSchemaDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataSchemas(String projectId, String experimentId, String runId) {
        runDataSchemaRepository.deleteByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
    }
}

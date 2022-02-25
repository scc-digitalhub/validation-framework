package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
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
    
    // Run
    public RunDTO createRun(String projectId, RunDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDTO> findRuns(String projectId, Optional<String> experimentName) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDTO findRunById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRun(String projectId, String id) {
        // TODO Auto-generated method stub
    }
    
    // RunMetadata
    public RunMetadataDTO createRunMetadata(String projectId, String runId, RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunMetadataDTO findRunMetadata(String projectId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunMetadataDTO updateRunMetadata(String projectId, String runId, RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunMetadata(String projectId, String runId) {
        // TODO Auto-generated method stub
    }
    
    // RunEnvironment
    public RunEnvironmentDTO createRunEnvironment(String projectId, String runId, RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunEnvironmentDTO findRunEnvironment(String projectId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunEnvironmentDTO updateRunEnvironment(String projectId, String runId, RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunEnvironment(String projectId, String runId) {
        // TODO Auto-generated method stub
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
    public List<RunDataProfileDTO> createRunDataProfiles(String projectId, String runId, String result, List<RunDataProfileDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDataProfileDTO> findRunDataProfiles(String projectId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunDataProfileDTO findRunDataProfileById(String projectId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findProfileResult(String projectId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunDataProfileDTO> updateRunDataProfiles(String projectId, String runId, String result, List<RunDataProfileDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataProfiles(String projectId, String runId) {
        // TODO Auto-generated method stub
    }
    
    // RunValidationReport
    public List<RunValidationReportDTO> createRunValidationReports(String projectId, String runId, String result, List<RunValidationReportDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunValidationReportDTO> findRunValidationReports(String projectId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunValidationReportDTO findRunValidationReportById(String projectId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findValidationResult(String projectId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunValidationReportDTO> updateRunValidationReports(String projectId, String runId, String result, List<RunValidationReportDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunValidationReports(String projectId, String runId) {
        // TODO Auto-generated method stub
    }
    
    // RunDataSchema
    public List<RunDataSchemaDTO> createRunDataSchemas(String projectId, String runId, String result, List<RunDataSchemaDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<RunDataSchemaDTO> findRunDataSchemas(String projectId, String runId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public RunDataSchemaDTO findRunDataSchemaById(String projectId, String runId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public String findSchemaResult(String projectId, String runId) {
     // TODO Auto-generated method stub
        return null;
    }
   
    public List<RunDataSchemaDTO> updateRunDataSchemas(String projectId, String runId, String result, List<RunDataSchemaDTO> reports) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataSchemas(String projectId, String runId) {
        // TODO Auto-generated method stub
    }
}

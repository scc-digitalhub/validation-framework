package it.smartcommunitylab.validationstorage.service;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.dto.ArtifactMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataProfileDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunMetadataDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunShortReportDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunShortSchemaDTO;
import it.smartcommunitylab.validationstorage.repository.ArtifactMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunDataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.RunEnvironmentRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.RunRepository;
import it.smartcommunitylab.validationstorage.repository.RunShortReportRepository;
import it.smartcommunitylab.validationstorage.repository.RunShortSchemaRepository;

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
    private RunDataResourceRepository runDataResourceRepository;
    
    @Autowired
    private RunShortReportRepository runShortReportRepository;
    
    @Autowired
    private RunShortSchemaRepository runShortSchemaRepository;
    
    // Run
    public RunDTO createRun(RunDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDTO findRunById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDTO updateRun(String id, RunDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRun(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunMetadata
    public RunMetadataDTO createRunMetadata(RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunMetadataDTO findRunMetadataById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunMetadataDTO updateRunMetadata(String id, RunMetadataDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunMetadata(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunEnvironment
    public RunEnvironmentDTO createRunEnvironment(RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunEnvironmentDTO findRunEnvironmentById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunEnvironmentDTO updateRunEnvironment(String id, RunEnvironmentDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunEnvironment(String id) {
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
    public RunDataProfileDTO createRunDataProfile(RunDataProfileDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDataProfileDTO findRunDataProfileById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDataProfileDTO updateRunDataProfile(String id, RunDataProfileDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataProfile(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunDataResource
    public RunDataResourceDTO createRunDataResource(RunDataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDataResourceDTO findRunDataResourceById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunDataResourceDTO updateRunDataResource(String id, RunDataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunDataResource(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunShortReport
    public RunShortReportDTO createRunShortReport(RunShortReportDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunShortReportDTO findRunShortReportById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunShortReportDTO updateRunShortReport(String id, RunShortReportDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunShortReport(String id) {
        // TODO Auto-generated method stub
    }
    
    // RunShortSchema
    public RunShortSchemaDTO createRunShortSchema(RunShortSchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunShortSchemaDTO findRunShortSchemaById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public RunShortSchemaDTO updateRunShortSchema(String id, RunShortSchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteRunShortSchema(String id) {
        // TODO Auto-generated method stub
    }
}

package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.RunConfig;
import it.smartcommunitylab.validationstorage.model.dto.RunConfigDTO;
import it.smartcommunitylab.validationstorage.repository.RunConfigRepository;

public class RunConfigService {
    @Autowired
    private RunConfigRepository repository;
    
    public RunConfig create(String projectId, @Valid RunConfigDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<RunConfig> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public RunConfig findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public RunConfig update(String projectId, String id, @Valid RunConfigDTO request) {
        // TODO Auto-generated method stub
        return null;
    }

    public void deleteById(String projectId, String id) {
        // TODO Auto-generated method stub
    }

    public void deleteByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId) {
        // TODO Auto-generated method stub
    }
}

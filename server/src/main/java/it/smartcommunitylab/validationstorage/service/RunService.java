package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.repository.RunRepository;

public class RunService {
    @Autowired
    private RunRepository repository;
    
    public Run create(String projectId, @Valid RunDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<Run> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public Run findById(String projectId, String id) {
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

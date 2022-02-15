package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.repository.ConstraintRepository;

public class ConstraintService {
    @Autowired
    private ConstraintRepository repository;
    
    public Constraint create(String projectId, @Valid ConstraintDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<Constraint> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public Constraint findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public Constraint update(String projectId, String id, @Valid ConstraintDTO request) {
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

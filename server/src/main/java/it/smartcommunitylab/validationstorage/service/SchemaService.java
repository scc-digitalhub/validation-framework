package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.Schema;
import it.smartcommunitylab.validationstorage.model.dto.SchemaDTO;
import it.smartcommunitylab.validationstorage.repository.SchemaRepository;

public class SchemaService {
    @Autowired
    private SchemaRepository repository;
    
    public Schema create(String projectId, @Valid SchemaDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<Schema> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public Schema findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public Schema update(String projectId, String id, @Valid SchemaDTO request) {
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

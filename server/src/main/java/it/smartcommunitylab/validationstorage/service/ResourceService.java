package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.Resource;
import it.smartcommunitylab.validationstorage.model.dto.ResourceDTO;
import it.smartcommunitylab.validationstorage.repository.ResourceRepository;

public class ResourceService {
    @Autowired
    private ResourceRepository repository;

    public Resource create(String projectId, @Valid ResourceDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<Resource> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public Resource findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public Resource update(String projectId, String id, @Valid ResourceDTO request) {
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

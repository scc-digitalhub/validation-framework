package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;

public class DataResourceService {
    @Autowired
    private DataResourceRepository repository;

    public DataResource create(String projectId, @Valid DataResourceDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<DataResource> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public DataResource findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public DataResource update(String projectId, String id, @Valid DataResourceDTO request) {
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

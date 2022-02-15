package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.repository.StoreRepository;

public class StoreService {
    @Autowired
    private StoreRepository repository;
    
    public Store create(String projectId, @Valid StoreDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<Store> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public Store findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public Store update(String projectId, String id, @Valid StoreDTO request) {
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
